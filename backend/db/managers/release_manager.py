from datetime import datetime
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.managers.moderation_logs_manager import ModerationLogManager
from db.models.releases import Release, ReleaseStatus
from db.models.tracks import Track 

class ReleaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

# ------------ CRUD -------------------

    async def create_release(
        self, 
        title: str,
        owner_id: int, 
        release_date: datetime, 
        image: str | None = None
    ) -> Release:
       
        new_release = Release(
            owner_id=owner_id,
            title = title,
            release_date=release_date,
            image=image,
            status=ReleaseStatus.DRAFT
        )
        
        self.session.add(new_release)
        await self.session.commit()
        await self.session.refresh(new_release)
        return new_release

    async def get_release_by_id(self, release_id: int, load_tracks: bool = False) -> Release | None:
        stmt = select(Release).where(Release.id == release_id).options(selectinload(Release.tracks).selectinload(Track.contributors))
        return await self.session.scalar(stmt)
    
    async def get_release_by_search(self, query:str, limit:int = 20, offset:int = 0) -> list[Release]:
        title = f"%{query}%"
        stmt = (
            select(Release)
            .where(
                Release.title.ilike(title),
                Release.status == ReleaseStatus.PUBLISHED
            )
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()


    async def delete_release(self, release: Release) -> None:
        await self.session.delete(release)
        await self.session.commit()

    async def update_release_data(
        self, 
        release: Release, 
        title: str | None = None,
        image: str | None = None
    ) -> Release:
        if title:
            release.title = title
        if image is not None:
            release.image = image
            
        await self.session.commit()
        await self.session.refresh(release)
        return release

# ------------- ARTIST ------------------------------

    async def submit_for_moderation(self, release: Release) -> Release:
        if release.status != ReleaseStatus.DRAFT and release.status != ReleaseStatus.REJECTED:
            raise ValueError("Отправить на модерацию можно только черновик или отклоненный релиз")
            
        release.status = ReleaseStatus.PENDING
        await self.session.commit()
        await self.session.refresh(release)
        return release


    async def get_releases_by_status(
        self, 
        status: ReleaseStatus, 
        limit: int = 20, 
        offset: int = 0
    ) -> Sequence[Release]:
        stmt = (
            select(Release)
            .where(Release.status == status)
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()


# ------------- MODER --------------------------

    async def change_status(self, release: Release, new_status: ReleaseStatus, moderator_id:int, comment:str | None) -> Release:
        
        if new_status == ReleaseStatus.REJECTED:
            if not comment:
                raise ValueError("No comment")
            log_manager = ModerationLogManager(self.session)
            await log_manager.create_log(
                release_id=release.id,
                moderator_id=moderator_id,
                comment=comment,
                commit=False
                )

        release.status = new_status
        await self.session.commit()
        await self.session.refresh(release)
        return release