from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.track_contributors import TrackContributor, ContributorRole

class TrackContributorManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_contributor(
        self, 
        track_id: int, 
        role: ContributorRole, 
        user_id: int | None = None, 
        external_name: str | None = None
    ) -> TrackContributor:

        if not user_id and not external_name:
            raise ValueError("You must specify either the user_id or the external_name.")
        if user_id and external_name:
            external_name = None

        new_contributor = TrackContributor(
            track_id=track_id,
            user_id=user_id,
            external_name=external_name,
            role=role
        )
        
        self.session.add(new_contributor)
        await self.session.commit()
        await self.session.refresh(new_contributor)
        return new_contributor

    async def get_track_contributors(self, track_id: int) -> Sequence[TrackContributor]:
        stmt = select(TrackContributor).where(TrackContributor.track_id == track_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def remove_contributor(self, contributor_id: int) -> None:
        stmt = select(TrackContributor).where(TrackContributor.id == contributor_id)
        contributor = await self.session.scalar(stmt)
        if contributor:
            await self.session.delete(contributor)
            await self.session.commit()