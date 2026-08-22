from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.moderation_logs import HistoryKind, ModerationLog


class ModerationLogManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_log(
        self,
        release_id: int,
        moderator_id: int | None,
        action: str,
        comment: str | None = None,
        kind: HistoryKind = HistoryKind.MODERATION,
        commit: bool = True,
    ) -> ModerationLog:
        new_log = ModerationLog(
            release_id=release_id,
            moderator_id=moderator_id,
            action=action,
            comment=comment,
            kind=kind,
        )
        self.session.add(new_log)
        if commit:
            await self.session.commit()
            await self.session.refresh(new_log)
        return new_log

    async def get_logs_for_release(self, release_id: int) -> Sequence[ModerationLog]:
        stmt = (
            select(ModerationLog)
            .where(ModerationLog.release_id == release_id)
            .order_by(ModerationLog.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        return result.all()
