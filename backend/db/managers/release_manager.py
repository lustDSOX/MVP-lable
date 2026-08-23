from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.managers.moderation_logs_manager import ModerationLogManager
from db.managers.notification_manager import NotificationManager
from db.models.moderation_logs import HistoryKind
from db.models.notifications import NotifType
from db.models.releases import Release, ReleaseStatus, ReleaseType
from db.models.tracks import Track
from db.models.users import User, UserRole


class ReleaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_release(
        self,
        title: str,
        owner_id: int,
        release_date: datetime,
        image: str | None = None,
        type: ReleaseType = ReleaseType.SINGLE,
        genre: str | None = None,
        genres: list[str] | None = None,
        cover_note: str | None = None,
    ) -> Release:
        new_release = Release(
            owner_id=owner_id,
            title=title,
            release_date=release_date,
            image=image,
            type=type,
            genre=genre,
            genres=genres,
            cover_note=cover_note,
            status=ReleaseStatus.DRAFT,
        )
        self.session.add(new_release)
        await self.session.commit()
        await self.session.refresh(new_release)
        return new_release

    async def get_release_by_id(self, release_id: int, load_tracks: bool = False) -> Release | None:
        stmt = select(Release).where(Release.id == release_id).options(
            selectinload(Release.tracks).selectinload(Track.contributors),
            selectinload(Release.contract),
            selectinload(Release.moderation_logs),
            selectinload(Release.links),
        )
        return await self.session.scalar(stmt)

    async def get_release_by_search(self, query: str, limit: int = 20, offset: int = 0) -> list[Release]:
        title = f"%{query}%"
        stmt = (
            select(Release)
            .where(Release.title.ilike(title), Release.status == ReleaseStatus.PUBLISHED)
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.scalars(stmt)).all())

    async def delete_release(self, release: Release) -> None:
        await self.session.delete(release)
        await self.session.commit()

    async def update_release_data(
        self,
        release: Release,
        title: str | None = None,
        image: str | None = None,
        type: ReleaseType | None = None,
        genre: str | None = None,
        genres: list[str] | None = None,
        cover_note: str | None = None,
        release_date: datetime | None = None,
    ) -> Release:
        if title is not None:
            release.title = title
        if image is not None:
            release.image = image
        if type is not None:
            release.type = type
        if genre is not None:
            release.genre = genre
        if genres is not None:
            release.genres = genres
        if cover_note is not None:
            release.cover_note = cover_note
        if release_date is not None:
            release.release_date = release_date
        await self.session.commit()
        await self.session.refresh(release)
        return release

    async def submit_for_moderation(self, release: Release, actor_id: int | None = None) -> Release:
        allowed = {
            ReleaseStatus.DRAFT,
            ReleaseStatus.REJECTED,
            ReleaseStatus.CHANGES_REQUESTED,
        }
        if release.status not in allowed and not release.live_revision:
            raise ValueError("Отправить на модерацию можно только draft / rejected / changes_requested")
        release.status = ReleaseStatus.PENDING
        release.reject_reason = None
        release.change_request_note = None

        log_mgr = ModerationLogManager(self.session)
        await log_mgr.create_log(
            release_id=release.id,
            moderator_id=actor_id,
            action="submitted",
            comment=None,
            kind=HistoryKind.SUBMIT,
            commit=False,
        )

        notif = NotificationManager(self.session)
        mods = (
            await self.session.scalars(
                select(User).where(User.role.in_([UserRole.MODERATOR, UserRole.ADMIN]))
            )
        ).all()
        for m in mods:
            await notif.create(
                user_id=m.id,
                title="New release pending",
                body=f"«{release.title}» submitted for moderation",
                type=NotifType.RELEASE_PENDING,
                meta={"release_id": str(release.id)},
                commit=False,
            )

        await self.session.commit()
        await self.session.refresh(release)
        return release

    async def get_releases_by_status(
        self, status: ReleaseStatus, limit: int = 20, offset: int = 0
    ) -> Sequence[Release]:
        stmt = (
            select(Release)
            .where(Release.status == status)
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.scalars(stmt)).all()

    async def get_releases_by_owner(
        self, owner_id: int, limit: int = 50, offset: int = 0
    ) -> Sequence[Release]:
        stmt = (
            select(Release)
            .where(Release.owner_id == owner_id)
            .options(selectinload(Release.contract), selectinload(Release.tracks))
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.scalars(stmt)).all()

    async def change_status(
        self,
        release: Release,
        new_status: ReleaseStatus,
        moderator_id: int,
        comment: str | None,
    ) -> Release:
        if new_status in (ReleaseStatus.REJECTED, ReleaseStatus.CHANGES_REQUESTED) and not comment:
            raise ValueError("Comment is required when rejecting or requesting changes")

        log_manager = ModerationLogManager(self.session)
        await log_manager.create_log(
            release_id=release.id,
            moderator_id=moderator_id,
            action=new_status.value,
            comment=comment,
            kind=HistoryKind.MODERATION,
            commit=False,
        )

        release.status = new_status
        if new_status == ReleaseStatus.REJECTED:
            release.reject_reason = comment
            release.change_request_note = None
        elif new_status == ReleaseStatus.CHANGES_REQUESTED:
            release.change_request_note = comment
            release.reject_reason = comment
        elif new_status == ReleaseStatus.PUBLISHED:
            release.live_revision = False
            release.reject_reason = None
            release.change_request_note = None
        else:
            release.reject_reason = None
            release.change_request_note = None

        notif = NotificationManager(self.session)
        ntype = NotifType.MODERATION_DECISION
        if new_status == ReleaseStatus.CHANGES_REQUESTED:
            ntype = NotifType.CHANGE_REQUEST
        await notif.create(
            user_id=release.owner_id,
            title=f"Release {new_status.value}",
            body=comment or f"Status → {new_status.value}",
            type=ntype,
            meta={"release_id": str(release.id), "status": new_status.value},
            commit=False,
        )

        await self.session.commit()
        await self.session.refresh(release)
        return release

    async def mark_live_revision(self, release: Release) -> Release:
        release.live_revision = True
        release.status = ReleaseStatus.PENDING
        await self.session.commit()
        await self.session.refresh(release)
        return release

    async def list_published(self, limit: int = 20, offset: int = 0) -> Sequence[Release]:
        stmt = (
            select(Release)
            .where(Release.status == ReleaseStatus.PUBLISHED)
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.scalars(stmt)).all()
