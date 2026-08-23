from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from auth import Current_User_Dep, DB_Dep, get_current_user
from db.managers.contract_manager import ContractManager
from db.managers.release_manager import ReleaseManager
from db.models.contracts import ContractStatus
from services.contract_pdf import generate_contract_pdf


class ContractCreate(BaseModel):
    release_id: int
    version: str = "v0.3"
    file_url: str | None = None


class ContractSign(BaseModel):
    artist_full_name: str
    file_url: str | None = None


class ContractResponse(BaseModel):
    id: int
    release_id: int
    status: ContractStatus
    version: str
    artist_full_name: str | None = None
    file_url: str | None = None
    signed_at: str | None = None

    model_config = ConfigDict(from_attributes=True)


async def get_contract_manager(db: DB_Dep) -> ContractManager:
    return ContractManager(db)


async def get_release_manager(db: DB_Dep) -> ReleaseManager:
    return ReleaseManager(db)


Manager_Dep = Annotated[ContractManager, Depends(get_contract_manager)]
ReleaseMgr_Dep = Annotated[ReleaseManager, Depends(get_release_manager)]

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    data: ContractCreate,
    manager: Manager_Dep,
    release_mgr: ReleaseMgr_Dep,
    current_user: Current_User_Dep,
):
    release = await release_mgr.get_release_by_id(data.release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    if release.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    file_url = data.file_url
    if not file_url:
        file_url = generate_contract_pdf(
            release_id=release.id,
            release_title=release.title,
            artist_full_name=current_user.full_name
            or current_user.artist_name
            or current_user.username
            or "",
            version=data.version,
        )
    return await manager.create_for_release(
        release_id=data.release_id,
        version=data.version,
        file_url=file_url,
    )


@router.get("/by-release/{release_id}", response_model=ContractResponse)
async def get_contract_by_release(
    release_id: int,
    manager: Manager_Dep,
    release_mgr: ReleaseMgr_Dep,
    current_user: Current_User_Dep,
):
    release = await release_mgr.get_release_by_id(release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    if release.owner_id != current_user.id and current_user.role.value not in (
        "moderator",
        "admin",
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    contract = await manager.get_by_release(release_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.post("/{contract_id}/sign", response_model=ContractResponse)
async def sign_contract(
    contract_id: int,
    data: ContractSign,
    manager: Manager_Dep,
    release_mgr: ReleaseMgr_Dep,
    current_user: Current_User_Dep,
):
    contract = await manager.get_by_id(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    release = await release_mgr.get_release_by_id(contract.release_id)
    if not release or release.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await manager.sign(contract, data.artist_full_name, data.file_url)


@router.post("/{contract_id}/needs-resign", response_model=ContractResponse)
async def mark_needs_resign(
    contract_id: int,
    manager: Manager_Dep,
    release_mgr: ReleaseMgr_Dep,
    current_user: Current_User_Dep,
):
    contract = await manager.get_by_id(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    release = await release_mgr.get_release_by_id(contract.release_id)
    if not release or release.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await manager.mark_needs_resign(contract)
