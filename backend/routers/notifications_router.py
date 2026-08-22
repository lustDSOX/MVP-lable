from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from auth import AdminDep, Current_User_Dep, DB_Dep, get_current_user
from db.managers.notification_manager import NotificationManager
from db.models.notifications import NotifType


class NotificationCreate(BaseModel):
    user_id: int
    title: str
    body: str
    type: NotifType = NotifType.ADMIN_MESSAGE
    meta: dict[str, Any] | None = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    type: NotifType
    read: bool
    meta: dict[str, Any] | None = None
    created_at: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UnreadCount(BaseModel):
    count: int


async def get_notif_manager(db: DB_Dep) -> NotificationManager:
    return NotificationManager(db)


Mgr = Annotated[NotificationManager, Depends(get_notif_manager)]

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[NotificationResponse])
async def list_my_notifications(
    mgr: Mgr,
    current_user: Current_User_Dep,
    limit: int = 100,
    offset: int = 0,
    unread_only: bool = False,
):
    return await mgr.list_for_user(
        current_user.id, limit=limit, offset=offset, unread_only=unread_only
    )


@router.get("/unread-count", response_model=UnreadCount)
async def unread_count(mgr: Mgr, current_user: Current_User_Dep):
    c = await mgr.unread_count(current_user.id)
    return UnreadCount(count=c)


@router.post("/{notif_id}/read", response_model=NotificationResponse)
async def mark_read(notif_id: int, mgr: Mgr, current_user: Current_User_Dep):
    n = await mgr.mark_read(notif_id, current_user.id)
    if not n:
        raise HTTPException(404, "Not found")
    return n


@router.post("/read-all", response_model=UnreadCount)
async def mark_all_read(mgr: Mgr, current_user: Current_User_Dep):
    c = await mgr.mark_all_read(current_user.id)
    return UnreadCount(count=c)


@router.post("/", response_model=NotificationResponse, status_code=201)
async def create_notification(
    data: NotificationCreate,
    mgr: Mgr,
    _: AdminDep,
):
    return await mgr.create(
        user_id=data.user_id,
        title=data.title,
        body=data.body,
        type=data.type,
        meta=data.meta,
    )
