import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text, func

from db.database import Base


class CmsStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class NewsItem(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    excerpt = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    date = Column(String, nullable=True)
    status = Column(Enum(CmsStatus), default=CmsStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class EventItem(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    venue = Column(String, nullable=True)
    city = Column(String, nullable=True)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    ticket_url = Column(String, nullable=True)
    price = Column(String, nullable=True)
    capacity = Column(String, nullable=True)
    age_limit = Column(String, nullable=True)
    status = Column(Enum(CmsStatus), default=CmsStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class GuideItem(Base):
    __tablename__ = "guides"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    excerpt = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    category = Column(String, default="general", nullable=False)
    status = Column(Enum(CmsStatus), default=CmsStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
