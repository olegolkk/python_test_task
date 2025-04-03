import uuid
from typing import Any

from sqlalchemy.orm import Mapped, DeclarativeBase, declared_attr, relationship
from sqlalchemy import Column, UUID, DateTime, Float, Integer, String, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True)
    created_on: Mapped[datetime] = Column(DateTime, default=datetime.utcnow())

    devices = relationship("DeviceStats", back_populates="user")

class DeviceStats(Base):
    __tablename__ = "device_stats"

    device_id: Mapped[int] = Column(Integer, nullable=False)
    timestamp: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    x: Mapped[float] = Column(Float)
    y: Mapped[float] = Column(Float)
    z: Mapped[float] = Column(Float)

    user_id = Column(UUID, ForeignKey('users.id'))

    user = relationship("User", back_populates="devices")