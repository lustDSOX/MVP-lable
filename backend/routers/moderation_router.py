from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict

from auth import DB_Dep, ModeratorDep, get_current_user
from db.managers.release_manager import ReleaseManager
from db.managers.moderation_logs_manager import ModerationLogManager
from db.models.moderation_logs import HistoryKind
from db.models.releases import ReleaseStatus


class ReleaseResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    image: str | None
    release_date: datetime
    status: ReleaseStatus
    reject_reason: str | None = None
    change_request_note: str | None = None
    live_revision: bool = False

    model_config = ConfigDict(from_attributes=True)


class ModerationLogResponse(BaseModel):
    id: int
    release_id: int
    moderator_id: int | None
    action: str
    comment: str | None
    kind: HistoryKind = HistoryKind.MODERATION
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class LogCreate(BaseModel):
    action: str
    comment: str | None = None
    kind: HistoryKind = HistoryKind.SYSTEM


async def get_release_manager(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


async def get_log_manager(db: DB_Dep) -> ModerationLogManager:
    return ModerationLogManager(db)


ReleaseMgr = Annotated[ReleaseManager, Depends(get_release_manager)]
LogMgr = Annotated[ModerationLogManager, Depends(get_log_manager)]

router = APIRouter(
    prefix="/moderation",
    tags=["Moderation"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/queue", response_model=list[ReleaseResponse])
async def moderation_queue(
    _: ModeratorDep,
    manager: ReleaseMgr,
    status_filter: ReleaseStatus = Query(default=ReleaseStatus.PENDING, alias="status"),
    limit: int = 20,
    offset: int = 0,
):
    return await manager.get_releases_by_status(status=status_filter, limit=limit, offset=offset)


@router.get("/releases/{release_id}/logs", response_model=list[ModerationLogResponse])
async def release_moderation_logs(
    release_id: int,
    logs: LogMgr,
    current_user=Depends(get_current_user),
):
    return await logs.get_logs_for_release(release_id)


@router.post("/releases/{release_id}/logs", response_model=ModerationLogResponse, status_code=201)
async def add_log(
    release_id: int,
    data: LogCreate,
    logs: LogMgr,
    manager: ReleaseMgr,
    current_user=Depends(get_current_user),
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(404, "Release not found")
    is_owner = release.owner_id == current_user.id
    is_staff = current_user.role.value in ("moderator", "admin")
    if not is_owner and not is_staff:
        raise HTTPException(403, "Forbidden")
    return await logs.create_log(
        release_id=release_id,
        moderator_id=current_user.id,
        action=data.action,
        comment=data.comment,
        kind=data.kind,
    )
