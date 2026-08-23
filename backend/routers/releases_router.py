from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict

from auth import Current_User_Dep, DB_Dep, ModeratorDep, get_current_user
from db.managers.release_manager import ReleaseManager
from db.models.releases import ReleaseStatus, ReleaseType


class ReleaseBase(BaseModel):
    title: str
    image: str | None = None
    cover_note: str | None = None
    type: ReleaseType = ReleaseType.SINGLE
    genre: str | None = None
    genres: list[str] | None = None


class ReleaseCreate(ReleaseBase):
    release_date: datetime


class ReleaseUpdate(BaseModel):
    title: str | None = None
    image: str | None = None
    cover_note: str | None = None
    type: ReleaseType | None = None
    genre: str | None = None
    genres: list[str] | None = None
    release_date: datetime | None = None


class ReleaseStatusUpdate(BaseModel):
    new_status: ReleaseStatus
    comment: str | None = None


class ContractBrief(BaseModel):
    id: int
    status: str
    version: str
    artist_full_name: str | None = None
    file_url: str | None = None
    signed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ReleaseResponse(ReleaseBase):
    id: int
    owner_id: int
    release_date: datetime
    status: ReleaseStatus
    reject_reason: str | None = None
    change_request_note: str | None = None
    live_revision: bool = False
    contract: ContractBrief | None = None

    model_config = ConfigDict(from_attributes=True)


async def get_release_manager(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


Manager_Dep = Annotated[ReleaseManager, Depends(get_release_manager)]

router = APIRouter(prefix="/releases", tags=["Releases"])

protect_router = APIRouter(
    prefix="/releases",
    tags=["Releases"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[ReleaseResponse])
async def list_published_releases(manager: Manager_Dep, limit: int = 20, offset: int = 0):
    return await manager.list_published(limit=limit, offset=offset)


@router.get("/search", response_model=list[ReleaseResponse])
async def search_releases(
    manager: Manager_Dep,
    query: str = Query(..., min_length=3),
    limit: int = 20,
    offset: int = 0,
):
    return await manager.get_release_by_search(query, limit, offset)


@router.get("/{release_id}", response_model=ReleaseResponse)
async def get_release(release_id: int, manager: Manager_Dep):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    if release.status != ReleaseStatus.PUBLISHED:
        raise HTTPException(status_code=403, detail="Release is not published yet")
    return release


@protect_router.post("/", response_model=ReleaseResponse, status_code=201)
async def create_release(
    data: ReleaseCreate, manager: Manager_Dep, current_user: Current_User_Dep
):
    return await manager.create_release(
        title=data.title,
        owner_id=current_user.id,
        release_date=data.release_date,
        image=data.image,
        type=data.type,
        genre=data.genre,
        genres=data.genres,
        cover_note=data.cover_note,
    )


@protect_router.get("/mine", response_model=list[ReleaseResponse])
async def my_releases(
    manager: Manager_Dep, current_user: Current_User_Dep, limit: int = 50, offset: int = 0
):
    return await manager.get_releases_by_owner(current_user.id, limit=limit, offset=offset)


@protect_router.patch("/{release_id}", response_model=ReleaseResponse)
async def update_release(
    release_id: int,
    data: ReleaseUpdate,
    manager: Manager_Dep,
    current_user: Current_User_Dep,
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    return await manager.update_release_data(
        release,
        title=data.title,
        image=data.image,
        type=data.type,
        genre=data.genre,
        genres=data.genres,
        cover_note=data.cover_note,
        release_date=data.release_date,
    )


@protect_router.delete("/{release_id}", status_code=204)
async def delete_release(
    release_id: int, manager: Manager_Dep, current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    await manager.delete_release(release)


@protect_router.post("/{release_id}/submit", response_model=ReleaseResponse)
async def submit_release_for_moderation(
    release_id: int, manager: Manager_Dep, current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    try:
        return await manager.submit_for_moderation(release, actor_id=current_user.id)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@protect_router.get("/status/{status_val}", response_model=list[ReleaseResponse])
async def get_releases_by_status(
    status_val: ReleaseStatus,
    manager: Manager_Dep,
    _: ModeratorDep,
    limit: int = 20,
    offset: int = 0,
):
    return await manager.get_releases_by_status(status=status_val, limit=limit, offset=offset)


@protect_router.get("/{release_id}/draft", response_model=ReleaseResponse)
async def get_my_draft_release(
    release_id: int, manager: Manager_Dep, current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    if release.owner_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    return release


@protect_router.patch("/{release_id}/status", response_model=ReleaseResponse)
async def change_release_status(
    release_id: int,
    data: ReleaseStatusUpdate,
    manager: Manager_Dep,
    moderator: ModeratorDep,
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    try:
        return await manager.change_status(
            release=release,
            new_status=data.new_status,
            moderator_id=moderator.id,
            comment=data.comment,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
