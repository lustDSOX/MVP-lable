from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from auth import Current_User_Dep, DB_Dep, get_current_user
from db.managers.release_manager import ReleaseManager
from db.managers.release_links_manager import ReleaseLinkManager
from db.models.release_links import Platform
from db.models.users import UserRole


class LinkCreate(BaseModel):
    platform: Platform
    link: str = Field(min_length=8)


class LinkResponse(BaseModel):
    id: int
    release_id: int
    platform: Platform
    link: str

    model_config = ConfigDict(from_attributes=True)


async def get_release_manager(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


async def get_links_manager(db: DB_Dep) -> ReleaseLinkManager:
    return ReleaseLinkManager(db)


ReleaseMgr = Annotated[ReleaseManager, Depends(get_release_manager)]
LinksMgr = Annotated[ReleaseLinkManager, Depends(get_links_manager)]

router = APIRouter(tags=["Release Links"])


@router.get("/releases/{release_id}/links", response_model=list[LinkResponse])
async def list_links(release_id: int, lm: LinksMgr, rm: ReleaseMgr):
    release = await rm.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return await lm.get_links_for_release(release_id)


@router.post(
    "/releases/{release_id}/links",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def add_link(
    release_id: int,
    data: LinkCreate,
    lm: LinksMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    release = await rm.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    is_staff = user.role in (UserRole.MODERATOR, UserRole.ADMIN)
    if release.owner_id != user.id and not is_staff:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await lm.set_link(release_id=release_id, platform=data.platform, link=data.link)


@router.delete(
    "/releases/{release_id}/links/{platform}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_link(
    release_id: int,
    platform: Platform,
    lm: LinksMgr,
    rm: ReleaseMgr,
    user: Current_User_Dep,
):
    release = await rm.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    is_staff = user.role in (UserRole.MODERATOR, UserRole.ADMIN)
    if release.owner_id != user.id and not is_staff:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await lm.remove_link(release_id, platform)
