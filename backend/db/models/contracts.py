import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from db.database import Base


class ContractStatus(str, enum.Enum):
    UNSIGNED = "unsigned"
    SIGNED = "signed"
    VOID = "void"
    NEEDS_RESIGN = "needs_resign"


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id", ondelete="CASCADE"), nullable=False, unique=True)
    status = Column(Enum(ContractStatus), default=ContractStatus.UNSIGNED, nullable=False)
    version = Column(String, default="v0.3", nullable=False)
    artist_full_name = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    signed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    release = relationship("Release", back_populates="contract")
