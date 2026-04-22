import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from database import Base
from sqlalchemy.orm import relationship

class ReleaseStatus(str, enum.Enum):
    DRAFT = "draft"                 # Артист еще заполняет данные
    PENDING = "pending"             # Отправлено на модерацию
    APPROVED = "approved"           # Одобрено модератором
    REJECTED = "rejected"           # Отклонено
    PUBLISHED = "published"         # Отправлено на площадки

class Release(Base):
    # Сингл, EP, Альбом
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(ReleaseStatus), default=ReleaseStatus.DRAFT, nullable=False)
    image = Column(String, nullable=True)
    release_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    owner = relationship('User', back_populates='releases')
    tracks = relationship('Track', back_populates='release', cascade='all, delete-orphan')
    moderation_logs = relationship('ModerationLog', back_populates='release', cascade='all, delete-orphan')
    links = relationship('ReleaseLink', back_populates='release', cascade='all, delete-orphan')