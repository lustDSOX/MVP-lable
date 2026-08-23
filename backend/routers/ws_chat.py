"""WebSocket staff chat. Auth via ?token=JWT query param."""

from __future__ import annotations

import json
import logging
from typing import Any

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import select

from auth import SECRET_KEY, ALGORITHM
from db.database import AsyncSessionLocal
from db.managers.user_manager import UserManager
from db.managers.chat_manager import ChatManager
from db.models.users import User

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Staff Chat WS"])


class ConnectionManager:
    def __init__(self):
        self.active: dict[int, set[WebSocket]] = {}

    async def connect(self, user_id: int, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(user_id, set()).add(ws)

    def disconnect(self, user_id: int, ws: WebSocket):
        peers = self.active.get(user_id)
        if peers:
            peers.discard(ws)
            if not peers:
                del self.active[user_id]

    async def send_to(self, user_id: int, payload: dict[str, Any]):
        dead: list[WebSocket] = []
        for ws in self.active.get(user_id, set()):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(user_id, ws)


manager = ConnectionManager()


async def _user_from_token(token: str) -> User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
    except jwt.InvalidTokenError:
        return None
    async with AsyncSessionLocal() as session:
        um = UserManager(session)
        return await um.get_user_by_username(username)


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket, token: str = Query(...)):
    user = await _user_from_token(token)
    if not user:
        await websocket.close(code=4401)
        return

    await manager.connect(user.id, websocket)
    try:
        await websocket.send_json({"type": "connected", "user_id": user.id})
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "detail": "invalid json"})
                continue

            if data.get("type") != "message":
                continue
            to_id = data.get("to_user_id")
            body = (data.get("body") or "").strip()
            if not to_id or not body:
                await websocket.send_json({"type": "error", "detail": "to_user_id and body required"})
                continue

            async with AsyncSessionLocal() as session:
                cm = ChatManager(session)
                msg = await cm.send(user.id, int(to_id), body[:4000])
                payload = {
                    "type": "message",
                    "id": msg.id,
                    "from_user_id": msg.from_user_id,
                    "to_user_id": msg.to_user_id,
                    "body": msg.body,
                    "created_at": msg.created_at.isoformat() if msg.created_at else None,
                }
            await manager.send_to(user.id, payload)
            await manager.send_to(int(to_id), payload)
    except WebSocketDisconnect:
        manager.disconnect(user.id, websocket)
    except Exception:
        logger.exception("ws chat error")
        manager.disconnect(user.id, websocket)
