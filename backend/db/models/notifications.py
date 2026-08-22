import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.database import Base


class NotifType(str, enum.Enum):
    RELEASE_PENDING = "release_pending"
    MODERATION_DECISION = "moderation_decision"
    CHANGE_REQUEST = "change_request"
    ADMIN_MESSAGE = "admin_message"
    SYSTEM = "system"
    CHAT_MENTION = "chat_mention"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    type = Column(Enum(NotifType), default=NotifType.SYSTEM, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    meta = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="notifications")
