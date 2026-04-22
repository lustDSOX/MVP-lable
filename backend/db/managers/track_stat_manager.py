from datetime import datetime, date
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.track_stats import TrackStat
from db.models.release_links import Platform

class TrackStatManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_or_update_daily_stat(
        self, 
        track_id: int, 
        platform: Platform, 
        stat_date: datetime, 
        stream_count: int
    ) -> TrackStat:

        stmt = select(TrackStat).where(
            TrackStat.track_id == track_id,
            TrackStat.platform == platform,
            TrackStat.date == stat_date
        )
        existing_stat = await self.session.scalar(stmt)

        if existing_stat:
            existing_stat.stream_count = stream_count
            await self.session.commit()
            await self.session.refresh(existing_stat)
            return existing_stat
        else:
            new_stat = TrackStat(
                track_id=track_id,
                platform=platform,
                date=stat_date,
                stream_count=stream_count
            )
            self.session.add(new_stat)
            await self.session.commit()
            await self.session.refresh(new_stat)
            return new_stat

    async def get_stats_for_track(self, track_id: int, platform: Platform | None = None) -> Sequence[TrackStat]:
        stmt = select(TrackStat).where(TrackStat.track_id == track_id)
        
        if platform:
            stmt = stmt.where(TrackStat.platform == platform)
            
        stmt = stmt.order_by(TrackStat.date.asc())
        
        result = await self.session.scalars(stmt)
        return result.all()