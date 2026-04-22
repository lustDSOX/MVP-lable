from sqlalchemy import  Column, Date, Enum, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

from models.release_links import Platform


class TrackStat(Base):
    __tablename__ = "track_stats"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey('tracks.id', ondelete='CASCADE'), nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    date = Column(Date, nullable=False) #за какую дату собрана стата
    stream_count = Column(Integer, nullable=False)

    track = relationship('Track', back_populates='stats')