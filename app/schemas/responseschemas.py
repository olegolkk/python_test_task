from schemas.requestschemas import DeviceStatsCreateSchema, UserCreateSchema
from datetime import datetime
from uuid import UUID

class DeviceStatsResponseSchema(DeviceStatsCreateSchema):
    id: UUID
    timestamp: datetime
    user_id: int

class UserResponseSchema(UserCreateSchema):
    id: UUID
    created_on: datetime