from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.release_links import ReleaseLink, Platform

class ReleaseLinkManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_link(self, release_id: int, platform: Platform, link: str) -> ReleaseLink:

        stmt = select(ReleaseLink).where(
            ReleaseLink.release_id == release_id,
            ReleaseLink.platform == platform
        )
        existing_link = await self.session.scalar(stmt)
        
        # если есть перезаписываем 
        if existing_link:
            existing_link.link = link
            await self.session.commit()
            await self.session.refresh(existing_link)
            return existing_link
        else:
            new_link = ReleaseLink(
                release_id=release_id,
                platform=platform,
                link=link
            )
            self.session.add(new_link)
            await self.session.commit()
            await self.session.refresh(new_link)
            return new_link

    async def get_links_for_release(self, release_id: int) -> Sequence[ReleaseLink]:
        stmt = select(ReleaseLink).where(ReleaseLink.release_id == release_id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def remove_link(self, release_id: int, platform: Platform) -> None:
        stmt = select(ReleaseLink).where(
            ReleaseLink.release_id == release_id,
            ReleaseLink.platform == platform
        )
        link = await self.session.scalar(stmt)
        
        if link:
            await self.session.delete(link)
            await self.session.commit()