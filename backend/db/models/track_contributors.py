import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship


class ContributorRole(str, enum.Enum):
    MAIN_ARTIST = "main_artist"
    FEATURED = "featured"
    PRODUCER = "producer"
    SONGWRITER = "songwriter"
    OTHER = "other"


class TrackContributor(Base):
    __tablename__ = "track_contributors"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    role = Column(Enum(ContributorRole), nullable=False)
    credit_name = Column(String, nullable=True)

    track = relationship("Track", back_populates="contributors")
    user = relationship("User", back_populates="contributions")
