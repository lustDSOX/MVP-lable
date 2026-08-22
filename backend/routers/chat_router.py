from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from auth import Current_User_Dep, DB_Dep, get_current_user
from db.managers.chat_manager import ChatManager
from db.managers.user_manager import UserManager


class SendMessage(BaseModel):
    to_user_id: int
    body: str = Field(..., min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    body: str
    created_at: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PeerResponse(BaseModel):
    id: int
    email: str
    username: str | None = None
    artist_name: str | None = None


async def get_chat_manager(db: DB_Dep) -> ChatManager:
    return ChatManager(db)


async def get_user_manager(db: DB_Dep) -> UserManager:
    return UserManager(db)


ChatMgr = Annotated[ChatManager, Depends(get_chat_manager)]
UserMgr = Annotated[UserManager, Depends(get_user_manager)]

router = APIRouter(
    prefix="/chat",
    tags=["Staff Chat"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/messages", response_model=MessageResponse, status_code=201)
async def send_message(
    data: SendMessage,
    mgr: ChatMgr,
    current_user: Current_User_Dep,
):
    if data.to_user_id == current_user.id:
        raise HTTPException(400, "Cannot message yourself")
    return await mgr.send(current_user.id, data.to_user_id, data.body)


@router.get("/thread/{peer_id}", response_model=list[MessageResponse])
async def get_thread(
    peer_id: int,
    mgr: ChatMgr,
    current_user: Current_User_Dep,
    limit: int = 200,
):
    return await mgr.thread(current_user.id, peer_id, limit=limit)


@router.get("/peers", response_model=list[PeerResponse])
async def list_peers(
    mgr: ChatMgr,
    user_mgr: UserMgr,
    current_user: Current_User_Dep,
):
    peer_ids = await mgr.peers_for(current_user.id)
    peers = []
    for pid in peer_ids:
        u = await user_mgr.get_user_by_id(pid) if hasattr(user_mgr, "get_user_by_id") else None
        if u:
            peers.append(
                PeerResponse(
                    id=u.id,
                    email=u.email,
                    username=u.username,
                    artist_name=u.artist_name,
                )
            )
    return peers


@router.get("/recent", response_model=list[MessageResponse])
async def recent_messages(
    mgr: ChatMgr,
    current_user: Current_User_Dep,
    limit: int = 50,
):
    return await mgr.recent_for_user(current_user.id, limit=limit)
