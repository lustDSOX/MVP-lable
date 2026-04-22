import enum

from sqlalchemy import Column, Enum, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    ARTIST = "artist"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    artist_name = Column(String, nullable=True)
    email = Column(String, unique=True,nullable=False)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.ARTIST)

    releases = relationship('Release', back_populates='owner', cascade='all, delete-orphan')
    contributions = relationship('TrackContributor', back_populates='user')