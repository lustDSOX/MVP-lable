from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.moderation_logs import ModerationLog 

class ModerationLogManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_log(
        self, 
        release_id: int, 
        moderator_id: int, 
        comment: str,
        commit:bool = True
    ) -> ModerationLog:
        new_log = ModerationLog(
            release_id=release_id,
            moderator_id=moderator_id,
            comment=comment
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