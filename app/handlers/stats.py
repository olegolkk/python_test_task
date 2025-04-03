from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from dependecy import get_device_stats_service
from fastapi import APIRouter, status, Depends
from schemas import DeviceStatsCreateSchema, UserCreateSchema
from service import DeviceStatsService


device_router = APIRouter(prefix="/api/devices", tags=["stats"])
user_router = APIRouter(prefix="/api/users", tags=["users"])

@device_router.post("/stats/{device_id}")
async def add_stats(
        device_stats_service: Annotated[DeviceStatsService, Depends(get_device_stats_service)],
        device_stats: DeviceStatsCreateSchema):
    return device_stats_service.create_device_stats(device_stats)

@device_router.get("/stats/{device_id}")
async def get_stats_by_device_id(
        device_stats_service: Annotated[DeviceStatsService, Depends(get_device_stats_service)],
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
):
    return device_stats_service.get_device_stats_by_device_id(device_id, start_time, end_time)

@device_router.get("/stats/{user_id}/all")
async def get_stats_all_by_user_id(
        device_stats_service: Annotated[DeviceStatsService, Depends(get_device_stats_service)],
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
):
    return device_stats_service.get_device_stats_all_by_user_id(user_id, start_time, end_time)

@device_router.get("/stats/{user_id}/{device_id}")
async def get_current_device_stats_by_user_id(
        device_stats_service: Annotated[DeviceStatsService, Depends(get_device_stats_service)],
        user_id: UUID,
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
):
    return device_stats_service.get_current_device_stats_by_user_id(user_id, device_id, start_time, end_time)

@user_router.post("")
async def create_user(
        device_stats_service: Annotated[DeviceStatsService, Depends(get_device_stats_service)],
        user: UserCreateSchema
):
    return device_stats_service.create_user(user)

@user_router.get("{user_id}")
async def get_user(
        device_stats_service: Annotated[DeviceStatsService, Depends(get_device_stats_service)],
        user_id: UUID
):
    return device_stats_service.get_user_by_id(user_id)