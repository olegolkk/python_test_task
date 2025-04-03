from uuid import UUID

from pydantic import BaseModel, Field

class Base(BaseModel):
    class Config:
        from_attributes=True

class DeviceStatsCreateSchema(Base):
    device_id: int
    x: float
    y: float
    z: float
    user_id: UUID

class UserCreateSchema(Base):
    name: str
    email: str