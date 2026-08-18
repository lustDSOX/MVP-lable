from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from auth import Current_User_Dep, DB_Dep, get_current_user
from db.managers.release_manager import ReleaseManager
from db.managers.tracks_manager import TrackManager
from db.managers.track_contributors_manager import TrackContributorManager
from db.models.track_contributors import ContributorRole
from db.models.releases import ReleaseStatus


class TrackCreate(BaseModel):
    title: str = Field(min_length=1)
    order: int = Field(ge=1)
    master_file: str = ""
    preview_file: str = ""
    lyrics: str = ""
    is_explicit: bool = False


class TrackUpdate(BaseModel):
    title: str | None = None
    lyrics: str | None = None
    is_explicit: bool | None = None
    order: int | None = Field(default=None, ge=1)
    master_file: str | None = None
    preview_file: str | None = None


class TrackResponse(BaseModel):
    id: int
    release_id: int
    title: str
    order: int
    master_file: str
    preview_file: str
    lyrics: str
    is_explicit: bool

    model_config = ConfigDict(from_attributes=True)


class ContributorCreate(BaseModel):
    role: ContributorRole
    user_id: int | None = None
    credit_name: str | None = None


class ContributorResponse(BaseModel):
    id: int
    track_id: int
    user_id: int | None
    role: ContributorRole
    credit_name: str | None

    model_config = ConfigDict(from_attributes=True)


async def get_track_manager(db: DB_Dep) -> TrackManager:
    return TrackManager(db)


async def get_release_manager(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


async def get_contrib_manager(db: DB_Dep) -> TrackContributorManager:
    return TrackContributorManager(db)


TrackMgr = Annotated[TrackManager, Depends(get_track_manager)]
ReleaseMgr = Annotated[ReleaseManager, Depends(get_release_manager)]
ContribMgr = Annotated[TrackContributorManager, Depends(get_contrib_manager)]

router = APIRouter(tags=["Tracks"], dependencies=[Depends(get_current_user)])


async def _owned_release(release_id: int, user_id: int, rm: ReleaseManager):
    release = await rm.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    if release.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if release.status not in (ReleaseStatus.DRAFT, ReleaseStatus.REJECTED):
        raise HTTPException(
            status_code=400,
            detail="Tracks can only be edited while draft or rejected",
        )
    return release


@router.get("/releases/{release_id}/tracks", response_model=list[TrackResponse])
async def list_tracks(
    release_id: int,
    tm: TrackMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    release = await rm.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    if release.owner_id != user.id and release.status != ReleaseStatus.PUBLISHED:
        from db.models.users import UserRole

        if user.role not in (UserRole.MODERATOR, UserRole.ADMIN):
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return await tm.get_tracks_for_release(release_id)


@router.post(
    "/releases/{release_id}/tracks",
    response_model=TrackResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_track(
    release_id: int,
    data: TrackCreate,
    tm: TrackMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    await _owned_release(release_id, user.id, rm)
    return await tm.create_track(
        release_id=release_id,
        title=data.title,
        order=data.order,
        master_file=data.master_file or "pending",
        preview_file=data.preview_file or "pending",
        lyrics=data.lyrics or "",
        is_explicit=data.is_explicit,
    )


@router.patch("/tracks/{track_id}", response_model=TrackResponse)
async def update_track(
    track_id: int,
    data: TrackUpdate,
    tm: TrackMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    track = await tm.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    await _owned_release(track.release_id, user.id, rm)
    updated = await tm.update_track_info(
        track,
        title=data.title,
        lyrics=data.lyrics,
        is_explicit=data.is_explicit,
        order=data.order,
    )
    if data.master_file is not None:
        updated.master_file = data.master_file
    if data.preview_file is not None:
        updated.preview_file = data.preview_file
    if data.master_file is not None or data.preview_file is not None:
        await tm.session.commit()
        await tm.session.refresh(updated)
    return updated


@router.delete("/tracks/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track(
    track_id: int,
    tm: TrackMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    track = await tm.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    await _owned_release(track.release_id, user.id, rm)
    await tm.delete_track(track)


@router.post(
    "/tracks/{track_id}/contributors",
    response_model=ContributorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_contributor(
    track_id: int,
    data: ContributorCreate,
    tm: TrackMgr,
    rm: ReleaseMgr,
    cm: ContribMgr,
    user: Current_User_Dep,
):
    track = await tm.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    await _owned_release(track.release_id, user.id, rm)
    try:
        return await cm.add_contributor(
            track_id=track_id,
            role=data.role,
            user_id=data.user_id,
            credit_name=data.credit_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tracks/{track_id}/contributors", response_model=list[ContributorResponse])
async def list_contributors(track_id: int, cm: ContribMgr, tm: TrackMgr):
    track = await tm.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return await cm.get_track_contributors(track_id)


@router.delete("/tracks/contributors/{contributor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contributor(
    contributor_id: int,
    cm: ContribMgr,
    tm: TrackMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    from sqlalchemy import select
    from db.models.track_contributors import TrackContributor

    stmt = select(TrackContributor).where(TrackContributor.id == contributor_id)
    contrib = await cm.session.scalar(stmt)
    if not contrib:
        raise HTTPException(status_code=404, detail="Contributor not found")
    track = await tm.get_track_by_id(contrib.track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    await _owned_release(track.release_id, user.id, rm)
    await cm.remove_contributor(contributor_id)
