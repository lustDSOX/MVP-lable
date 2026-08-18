from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from auth import DB_Dep, ModeratorDep, get_current_user
from db.managers.release_manager import ReleaseManager
from db.managers.moderation_logs_manager import ModerationLogManager
from db.models.releases import ReleaseStatus


class ReleaseResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    image: str | None
    release_date: datetime
    status: ReleaseStatus

    model_config = ConfigDict(from_attributes=True)


class ModerationLogResponse(BaseModel):
    id: int
    release_id: int
    moderator_id: int | None
    action: str
    comment: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


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
    _: ModeratorDep,
    logs: LogMgr,
):
    return await logs.get_logs_for_release(release_id)
