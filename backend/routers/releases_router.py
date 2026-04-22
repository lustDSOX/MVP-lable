from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from auth import Current_User_Dep, DB_Dep
from db.managers.release_manager import ReleaseManager
from db.models.releases import ReleaseStatus

class ReleaseBase(BaseModel):
    title: str
    image: str | None = None

class ReleaseCreate(ReleaseBase):
    release_date: datetime

class ReleaseUpdate(BaseModel):
    title: str | None = None
    image: str | None = None

class ReleaseStatusUpdate(BaseModel):
    new_status: ReleaseStatus
    comment: str | None = None

class ReleaseResponse(ReleaseBase):
    id: int
    owner_id: int
    release_date: datetime
    status: ReleaseStatus
    
    model_config = ConfigDict(from_attributes=True)


async def get_release_manager(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)

Manager_Dep = Annotated[ReleaseManager, Depends(get_release_manager)]


router = APIRouter(
    prefix="/releases", 
    tags=["Releases"]
)

protect_router = APIRouter(
    prefix="/releases",
    tags=["Releases"],
    dependencies=[Depends(Current_User_Dep)] 
)

# ----------- PUBLIC -------------------------

@router.get("/{release_id}", response_model=ReleaseResponse)
async def get_release(release_id: int, manager: Manager_Dep):
    release = await manager.get_release_by_id(release_id)

    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Release not found")
    if release.status != ReleaseStatus.PUBLISHED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Release is not published yet")
    
    return release

@router.get("/search", response_model=list[ReleaseResponse])
async def search_releases(
    manager: Manager_Dep,
    query: str = Query(..., min_length=3),
    limit: int = 20,
    offset: int = 0
):
    return await manager.search_releases_by_title(query, limit, offset)


# ----------- ARTIST ------------------------------

@protect_router.post("/", response_model=ReleaseResponse, status_code=status.HTTP_201_CREATED)
async def create_release(
    data: ReleaseCreate,
    manager: Manager_Dep,
    current_user: Current_User_Dep
):
    release = await manager.create_release(
        title=data.title,
        owner_id=current_user.id,
        release_date=data.release_date,
        image=data.image
    )
    return release


@protect_router.patch("/{release_id}", response_model=ReleaseResponse)
async def update_release(
    release_id: int,
    data: ReleaseUpdate,
    manager: Manager_Dep,
    current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    
    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Release not found")
    
    if release.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    updated_release = await manager.update_release_data(
        release=release,
        title=data.title,
        image=data.image
    )
    return updated_release

@protect_router.delete("/{release_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_release(
    release_id: int,
    manager: Manager_Dep,
    current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    
    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Release not found")
        
    if release.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    await manager.delete_release(release)

@protect_router.post("/{release_id}/submit", response_model=ReleaseResponse)
async def submit_release_for_moderation(
    release_id: int,
    manager: Manager_Dep,
    current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    
    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Release not found")
        
    if release.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    try:
        return await manager.submit_for_moderation(release)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@protect_router.get("/status/{status_val}", response_model=list[ReleaseResponse])
async def get_releases_by_status(
    status_val: ReleaseStatus,
    manager: Manager_Dep,
    limit: int = 20,
    offset: int = 0
):
    return await manager.get_releases_by_status(status=status_val, limit=limit, offset=offset)

@protect_router.get("/{release_id}/draft", response_model=ReleaseResponse)
async def get_my_draft_release(
    release_id: int, 
    manager: Manager_Dep,
    current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Release not found")
        
    if release.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
    return release



# --------------- MODERATOR ----------------------------
# TODO: В будущем здесь нужно добавить зависимость для проверки роли (is_moderator/is_admin)

@protect_router.patch("/{release_id}/status", response_model=ReleaseResponse)
async def change_release_status(
    release_id: int,
    data: ReleaseStatusUpdate,
    manager: Manager_Dep,
    current_user: Current_User_Dep
):
    release = await manager.get_release_by_id(release_id)
    
    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Release not found")
        
    try:
        return await manager.change_status(
            release=release,
            new_status=data.new_status,
            moderator_id=current_user.id,
            comment=data.comment
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))