import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from db.database import Base
from sqlalchemy.orm import relationship

class ReleaseStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"

class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    image = Column(String, nullable=True)
    status = Column(Enum(ReleaseStatus), default=ReleaseStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="releases")
    tracks = relationship("Track", back_populates="release", cascade="all, delete-orphan")
    links = relationship("ReleaseLink", back_populates="release", cascade="all, delete-orphan")
    moderation_logs = relationship("ModerationLog", back_populates="release", cascade="all, delete-orphan")
