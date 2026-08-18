from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey('releases.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    master_file = Column(String, nullable=False)
    preview_file = Column(String, nullable=False)
    lyrics = Column(String, nullable=False)
    is_explicit = Column(Boolean, nullable=False, default=False)

    release = relationship('Release', back_populates='tracks')
    contributors = relationship('TrackContributor', back_populates='track')
    stats = relationship('TrackStat', back_populates='track')
