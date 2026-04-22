import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Platform(str, enum.Enum):
    SPOTIFY = "spotify"
    YOUTUBE = "youtube"
    VK = "vk"
    YANDEX = "yandex"


class ReleaseLink(Base):
    __tablename__ = "release_links"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey('releases.id', ondelete="CASCADE"), nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    link = Column(String, nullable=False)

    release = relationship("Release", back_populates="links")