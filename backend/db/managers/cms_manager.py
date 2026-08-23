from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.cms import CmsStatus, EventItem, GuideItem, NewsItem


class CmsManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_news(
        self,
        status: CmsStatus | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[NewsItem]:
        stmt = select(NewsItem).order_by(NewsItem.updated_at.desc()).limit(limit).offset(offset)
        if status:
            stmt = stmt.where(NewsItem.status == status)
        return (await self.session.scalars(stmt)).all()

    async def get_news(self, item_id: int) -> NewsItem | None:
        return await self.session.scalar(select(NewsItem).where(NewsItem.id == item_id))

    async def create_news(self, **kwargs) -> NewsItem:
        item = NewsItem(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update_news(self, item: NewsItem, **kwargs) -> NewsItem:
        for k, v in kwargs.items():
            if v is not None and hasattr(item, k):
                setattr(item, k, v)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_news(self, item: NewsItem) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def list_events(
        self,
        status: CmsStatus | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[EventItem]:
        stmt = select(EventItem).order_by(EventItem.updated_at.desc()).limit(limit).offset(offset)
        if status:
            stmt = stmt.where(EventItem.status == status)
        return (await self.session.scalars(stmt)).all()

    async def get_event(self, item_id: int) -> EventItem | None:
        return await self.session.scalar(select(EventItem).where(EventItem.id == item_id))

    async def create_event(self, **kwargs) -> EventItem:
        item = EventItem(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update_event(self, item: EventItem, **kwargs) -> EventItem:
        for k, v in kwargs.items():
            if v is not None and hasattr(item, k):
                setattr(item, k, v)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_event(self, item: EventItem) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def list_guides(
        self,
        status: CmsStatus | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[GuideItem]:
        stmt = select(GuideItem).order_by(GuideItem.updated_at.desc()).limit(limit).offset(offset)
        if status:
            stmt = stmt.where(GuideItem.status == status)
        return (await self.session.scalars(stmt)).all()

    async def get_guide(self, item_id: int) -> GuideItem | None:
        return await self.session.scalar(select(GuideItem).where(GuideItem.id == item_id))

    async def create_guide(self, **kwargs) -> GuideItem:
        item = GuideItem(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update_guide(self, item: GuideItem, **kwargs) -> GuideItem:
        for k, v in kwargs.items():
            if v is not None and hasattr(item, k):
                setattr(item, k, v)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_guide(self, item: GuideItem) -> None:
        await self.session.delete(item)
        await self.session.commit()
