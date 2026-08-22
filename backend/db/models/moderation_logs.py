import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from db.database import Base


class HistoryKind(str, enum.Enum):
    MODERATION = "moderation"
    ARTIST_EDIT = "artist_edit"
    CONTRACT = "contract"
    SUBMIT = "submit"
    SYSTEM = "system"


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id", ondelete="CASCADE"), nullable=False)
    moderator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    kind = Column(Enum(HistoryKind), default=HistoryKind.MODERATION, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    release = relationship("Release", back_populates="moderation_logs")
