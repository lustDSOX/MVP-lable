from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.notifications import Notification, NotifType


class NotificationManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        title: str,
        body: str,
        type: NotifType = NotifType.SYSTEM,
        meta: dict | None = None,
        commit: bool = True,
    ) -> Notification:
        n = Notification(
            user_id=user_id,
            title=title,
            body=body,
            type=type,
            meta=meta,
        )
        self.session.add(n)
        if commit:
            await self.session.commit()
            await self.session.refresh(n)
        return n

    async def list_for_user(
        self,
        user_id: int,
        limit: int = 100,
        offset: int = 0,
        unread_only: bool = False,
    ) -> Sequence[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if unread_only:
            stmt = stmt.where(Notification.read.is_(False))
        return (await self.session.scalars(stmt)).all()

    async def unread_count(self, user_id: int) -> int:
        from sqlalchemy import func

        stmt = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.read.is_(False),
        )
        return await self.session.scalar(stmt) or 0

    async def mark_read(self, notif_id: int, user_id: int) -> Notification | None:
        n = await self.session.scalar(
            select(Notification).where(
                Notification.id == notif_id,
                Notification.user_id == user_id,
            )
        )
        if not n:
            return None
        n.read = True
        await self.session.commit()
        await self.session.refresh(n)
        return n

    async def mark_all_read(self, user_id: int) -> int:
        result = await self.session.execute(
            update(Notification)
            .where(Notification.user_id == user_id, Notification.read.is_(False))
            .values(read=True)
        )
        await self.session.commit()
        return result.rowcount or 0
