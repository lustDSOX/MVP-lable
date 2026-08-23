import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from db.database import Base


class ReleaseStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    CHANGES_REQUESTED = "changes_requested"


class ReleaseType(str, enum.Enum):
    SINGLE = "single"
    EP = "ep"
    ALBUM = "album"


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    image = Column(String, nullable=True)
    cover_note = Column(String, nullable=True)
    type = Column(Enum(ReleaseType), default=ReleaseType.SINGLE, nullable=False)
    genre = Column(String, nullable=True)
    genres = Column(ARRAY(String), nullable=True)
    status = Column(Enum(ReleaseStatus), default=ReleaseStatus.DRAFT, nullable=False)
    reject_reason = Column(Text, nullable=True)
    change_request_note = Column(Text, nullable=True)
    live_revision = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="releases")
    tracks = relationship("Track", back_populates="release", cascade="all, delete-orphan")
    links = relationship("ReleaseLink", back_populates="release", cascade="all, delete-orphan")
    moderation_logs = relationship("ModerationLog", back_populates="release", cascade="all, delete-orphan")
    contract = relationship("Contract", back_populates="release", uselist=False, cascade="all, delete-orphan")
