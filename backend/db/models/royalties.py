from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from db.database import Base
from db.models.release_links import Platform


class RoyaltyEntry(Base):
    """Per-release royalty snapshot (aggregated from platforms)."""

    __tablename__ = "royalty_entries"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String, default="RUB", nullable=False)
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    release = relationship("Release", backref="royalties")


class PlatformFollower(Base):
    """Follower counts per platform for a release (or artist-level later)."""

    __tablename__ = "platform_followers"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String, nullable=False)  # spotify, apple, yandex, vk
    followers = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    release = relationship("Release", backref="followers")
