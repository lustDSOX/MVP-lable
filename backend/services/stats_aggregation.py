"""Aggregate track_stats streams → royalty_entries estimate."""

from __future__ import annotations

from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.track_stats import TrackStat
from db.models.tracks import Track
from db.models.royalties import RoyaltyEntry

RATE_RUB = {
    "spotify": 0.35,
    "apple_music": 0.50,
    "apple": 0.50,
    "yandex": 0.25,
    "vk": 0.15,
    "youtube": 0.10,
    "other": 0.10,
}


async def estimate_royalties_for_release(
    session: AsyncSession,
    release_id: int,
    persist: bool = False,
    period_start: date | None = None,
    period_end: date | None = None,
) -> dict:
    track_ids = (
        await session.scalars(select(Track.id).where(Track.release_id == release_id))
    ).all()
    if not track_ids:
        return {"release_id": release_id, "total_streams": 0, "estimated_rub": 0.0, "by_platform": {}}

    stmt = (
        select(TrackStat.platform, func.sum(TrackStat.stream_count))
        .where(TrackStat.track_id.in_(track_ids))
        .group_by(TrackStat.platform)
    )
    if period_start:
        stmt = stmt.where(TrackStat.date >= period_start)
    if period_end:
        stmt = stmt.where(TrackStat.date <= period_end)

    rows = (await session.execute(stmt)).all()
    by_platform: dict[str, int] = {}
    estimated = 0.0
    total_streams = 0
    for platform, streams in rows:
        key = platform.value if hasattr(platform, "value") else str(platform)
        streams = int(streams or 0)
        by_platform[key] = streams
        total_streams += streams
        rate = RATE_RUB.get(key, RATE_RUB["other"])
        estimated += streams * rate

    if persist and estimated > 0:
        entry = RoyaltyEntry(
            release_id=release_id,
            amount=round(estimated, 2),
            currency="RUB",
            period_start=period_start,
            period_end=period_end,
            note="auto from track_stats",
        )
        session.add(entry)
        await session.commit()

    return {
        "release_id": release_id,
        "total_streams": total_streams,
        "estimated_rub": round(estimated, 2),
        "by_platform": by_platform,
    }
