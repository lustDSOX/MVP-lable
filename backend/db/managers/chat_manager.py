from typing import Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models.chat import ChatMessage


class ChatManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send(
        self,
        from_user_id: int,
        to_user_id: int,
        body: str,
    ) -> ChatMessage:
        msg = ChatMessage(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            body=body,
        )
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def thread(
        self,
        user_a: int,
        user_b: int,
        limit: int = 200,
    ) -> Sequence[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(
                or_(
                    (ChatMessage.from_user_id == user_a) & (ChatMessage.to_user_id == user_b),
                    (ChatMessage.from_user_id == user_b) & (ChatMessage.to_user_id == user_a),
                )
            )
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
        )
        return (await self.session.scalars(stmt)).all()

    async def peers_for(self, user_id: int) -> list[int]:
        stmt = select(ChatMessage).where(
            or_(ChatMessage.from_user_id == user_id, ChatMessage.to_user_id == user_id)
        )
        msgs = (await self.session.scalars(stmt)).all()
        peers: set[int] = set()
        for m in msgs:
            if m.from_user_id != user_id:
                peers.add(m.from_user_id)
            if m.to_user_id != user_id:
                peers.add(m.to_user_id)
        return sorted(peers)

    async def recent_for_user(
        self,
        user_id: int,
        limit: int = 50,
    ) -> Sequence[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(
                or_(ChatMessage.from_user_id == user_id, ChatMessage.to_user_id == user_id)
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        return (await self.session.scalars(stmt)).all()
