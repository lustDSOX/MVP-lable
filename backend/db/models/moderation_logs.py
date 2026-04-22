from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from database import Base
from sqlalchemy.orm import relationship


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey('releases.id', ondelete='CASCADE'), nullable=False)
    moderator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    release = relationship('Release', back_populates='moderation_logs')