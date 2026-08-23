from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from auth import AdminDep, Current_User_Dep, DB_Dep, ModeratorDep, get_current_user
from db.managers.release_manager import ReleaseManager
from db.managers.royalty_manager import RoyaltyManager
from services.stats_aggregation import estimate_royalties_for_release


class RoyaltyCreate(BaseModel):
    release_id: int
    amount: float
    currency: str = "RUB"
    period_start: date | None = None
    period_end: date | None = None
    note: str | None = None


class RoyaltyResponse(BaseModel):
    id: int
    release_id: int
    amount: float
    currency: str
    period_start: date | None = None
    period_end: date | None = None
    note: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FollowersUpdate(BaseModel):
    release_id: int
    followers: dict[str, int]


class FollowerResponse(BaseModel):
    platform: str
    followers: int

    model_config = ConfigDict(from_attributes=True)


class ReleaseStatsResponse(BaseModel):
    release_id: int
    total_royalties: float
    followers: list[FollowerResponse]


class EstimateResponse(BaseModel):
    release_id: int
    total_streams: int
    estimated_rub: float
    by_platform: dict[str, Any]


async def get_royalty_mgr(db: DB_Dep) -> RoyaltyManager:
    return RoyaltyManager(db)


async def get_release_mgr(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


RoyMgr = Annotated[RoyaltyManager, Depends(get_royalty_mgr)]
RelMgr = Annotated[ReleaseManager, Depends(get_release_mgr)]

router = APIRouter(
    prefix="/royalties",
    tags=["Royalties & Stats"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/release/{release_id}", response_model=ReleaseStatsResponse)
async def release_stats(
    release_id: int, roy: RoyMgr, rel: RelMgr, current_user: Current_User_Dep
):
    release = await rel.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id and current_user.role.value not in (
        "moderator",
        "admin",
    ):
        raise HTTPException(403, "Forbidden")
    total = await roy.total_for_release(release_id)
    followers = await roy.get_followers(release_id)
    return ReleaseStatsResponse(
        release_id=release_id,
        total_royalties=total,
        followers=[
            FollowerResponse(platform=f.platform, followers=f.followers) for f in followers
        ],
    )


@router.get("/release/{release_id}/entries", response_model=list[RoyaltyResponse])
async def list_entries(
    release_id: int, roy: RoyMgr, rel: RelMgr, current_user: Current_User_Dep
):
    release = await rel.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id and current_user.role.value not in (
        "moderator",
        "admin",
    ):
        raise HTTPException(403, "Forbidden")
    return await roy.list_for_release(release_id)


@router.post("/entries", response_model=RoyaltyResponse, status_code=201)
async def add_entry(data: RoyaltyCreate, roy: RoyMgr, _: AdminDep):
    return await roy.add_entry(
        release_id=data.release_id,
        amount=data.amount,
        currency=data.currency,
        period_start=data.period_start,
        period_end=data.period_end,
        note=data.note,
    )


@router.put("/followers", response_model=list[FollowerResponse])
async def set_followers(data: FollowersUpdate, roy: RoyMgr, _: ModeratorDep):
    rows = await roy.set_followers_bulk(data.release_id, data.followers)
    return [FollowerResponse(platform=r.platform, followers=r.followers) for r in rows]


@router.post("/release/{release_id}/estimate", response_model=EstimateResponse)
async def estimate_from_stats(
    release_id: int,
    rel: RelMgr,
    db: DB_Dep,
    current_user: Current_User_Dep,
    persist: bool = False,
    period_start: date | None = None,
    period_end: date | None = None,
):
    release = await rel.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id and current_user.role.value not in (
        "moderator",
        "admin",
    ):
        raise HTTPException(403, "Forbidden")
    if persist and current_user.role.value not in ("moderator", "admin"):
        raise HTTPException(403, "Only staff can persist estimates")
    data = await estimate_royalties_for_release(
        db, release_id, persist=persist, period_start=period_start, period_end=period_end
    )
    return EstimateResponse(**data)
