"""Track daily stream stats ingest (manual / future distributor feed)."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auth import AdminDep, Current_User_Dep, DB_Dep, ModeratorDep, get_current_user
from db.managers.track_stat_manager import TrackStatManager
from db.managers.tracks_manager import TrackManager
from db.managers.release_manager import ReleaseManager
from db.models.release_links import Platform


class StatIn(BaseModel):
    track_id: int
    platform: Platform
    date: date
    stream_count: int = Field(ge=0)


class StatOut(BaseModel):
    id: int
    track_id: int
    platform: Platform
    date: date
    stream_count: int

    model_config = ConfigDict(from_attributes=True)


async def get_tsm(db: DB_Dep) -> TrackStatManager:
    return TrackStatManager(db)


async def get_tm(db: DB_Dep) -> TrackManager:
    return TrackManager(db)


async def get_rm(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


TSM = Annotated[TrackStatManager, Depends(get_tsm)]
TM = Annotated[TrackManager, Depends(get_tm)]
RM = Annotated[ReleaseManager, Depends(get_rm)]

router = APIRouter(
    prefix="/stats",
    tags=["Track Stats"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=StatOut, status_code=201)
async def upsert_stat(data: StatIn, tsm: TSM, tm: TM, rm: RM, user: Current_User_Dep):
    track = await tm.get_track_by_id(data.track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    release = await rm.get_release_by_id(track.release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    is_staff = user.role.value in ("moderator", "admin")
    if release.owner_id != user.id and not is_staff:
        raise HTTPException(403, "Forbidden")
    from datetime import datetime

    dt = datetime.combine(data.date, datetime.min.time())
    return await tsm.add_or_update_daily_stat(
        track_id=data.track_id,
        platform=data.platform,
        stat_date=dt,
        stream_count=data.stream_count,
    )


@router.get("/track/{track_id}", response_model=list[StatOut])
async def list_track_stats(
    track_id: int,
    tsm: TSM,
    tm: TM,
    rm: RM,
    user: Current_User_Dep,
    platform: Platform | None = None,
):
    track = await tm.get_track_by_id(track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    release = await rm.get_release_by_id(track.release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != user.id and user.role.value not in ("moderator", "admin"):
        raise HTTPException(403, "Forbidden")
    return await tsm.get_stats_for_track(track_id, platform=platform)


@router.post("/bulk", response_model=list[StatOut], status_code=201)
async def bulk_stats(items: list[StatIn], tsm: TSM, _: ModeratorDep):
    from datetime import datetime

    out = []
    for data in items:
        dt = datetime.combine(data.date, datetime.min.time())
        row = await tsm.add_or_update_daily_stat(
            track_id=data.track_id,
            platform=data.platform,
            stat_date=dt,
            stream_count=data.stream_count,
        )
        out.append(row)
    return out
