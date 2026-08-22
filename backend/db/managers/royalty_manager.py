from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.royalties import PlatformFollower, RoyaltyEntry


class RoyaltyManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_for_release(self, release_id: int) -> Sequence[RoyaltyEntry]:
        stmt = (
            select(RoyaltyEntry)
            .where(RoyaltyEntry.release_id == release_id)
            .order_by(RoyaltyEntry.created_at.desc())
        )
        return (await self.session.scalars(stmt)).all()

    async def total_for_release(self, release_id: int) -> float:
        entries = await self.list_for_release(release_id)
        return sum(e.amount for e in entries)

    async def add_entry(
        self,
        release_id: int,
        amount: float,
        currency: str = "RUB",
        period_start: date | None = None,
        period_end: date | None = None,
        note: str | None = None,
    ) -> RoyaltyEntry:
        entry = RoyaltyEntry(
            release_id=release_id,
            amount=amount,
            currency=currency,
            period_start=period_start,
            period_end=period_end,
            note=note,
        )
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def get_followers(self, release_id: int) -> Sequence[PlatformFollower]:
        stmt = select(PlatformFollower).where(PlatformFollower.release_id == release_id)
        return (await self.session.scalars(stmt)).all()

    async def upsert_followers(
        self,
        release_id: int,
        platform: str,
        followers: int,
    ) -> PlatformFollower:
        stmt = select(PlatformFollower).where(
            PlatformFollower.release_id == release_id,
            PlatformFollower.platform == platform,
        )
        existing = await self.session.scalar(stmt)
        if existing:
            existing.followers = followers
            await self.session.commit()
            await self.session.refresh(existing)
            return existing
        row = PlatformFollower(
            release_id=release_id,
            platform=platform,
            followers=followers,
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def set_followers_bulk(
        self,
        release_id: int,
        data: dict[str, int],
    ) -> list[PlatformFollower]:
        result = []
        for platform, count in data.items():
            result.append(await self.upsert_followers(release_id, platform, count))
        return result
