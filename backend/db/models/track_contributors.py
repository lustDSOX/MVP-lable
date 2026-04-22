import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class ContributorRole(str, enum.Enum):
    MAIN_ARTIST = "main_artist"
    FEATURE = "feature"
    PRODUCER = "producer"
    WRITER = "writer"
    MIXING = "mixing"

class TrackContributor(Base):
    # Кто и что делал на конкретном треке
    __tablename__ = "track_contributors"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True) # только зарегистированные
    external_name = Column(String, nullable=True) # если не зарегистрирован, нет на сайте
    role = Column(Enum(ContributorRole), nullable=False)

    track = relationship("Track", back_populates="contributors")
    user = relationship("User", back_populates="contributions")
    

