from dataclasses import dataclass
from datetime import datetime

from fastapi import HTTPException, status
from repository import DeviceStatsRepository
from schemas import DeviceStatsCreateSchema, DeviceStatsResponseSchema, UserCreateSchema, UserResponseSchema

from uuid import UUID

@dataclass
class DeviceStatsService:
    device_stats_repository: DeviceStatsRepository

    # Создание записи о статистике по устройству
    def create_device_stats(self, device_stats: DeviceStatsCreateSchema) -> DeviceStatsResponseSchema:
        # Если такого пользователя нет, то выдаем ошибку
        if not self.device_stats_repository.get_user_by_id(device_stats.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Нет пользователя с таким ID",
            )
        id : UUID = self.device_stats_repository.create_device_stats(device_stats)
        return self.device_stats_repository.get_device_stats_by_id(id)

    # Получить статистику по id устройства
    def get_device_stats_by_device_id(self, device_id: int, start_time: datetime, end_time: datetime) -> dict:
        return self.device_stats_repository.get_device_stats_by_device_id(device_id, start_time, end_time)

    # Создать пользователя
    def create_user(self, user: UserCreateSchema) -> UserResponseSchema:
        if self.device_stats_repository.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Пользователь с таким email уже зарегистрирован",
            )
        user_id: UUID = self.device_stats_repository.create_user(user)
        return self.device_stats_repository.get_user_by_id(user_id)

    # Получить пользователя по id
    def get_user_by_id(self, user_id: UUID) -> UserResponseSchema:
        user = self.device_stats_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Нет пользователя с таким ID",
            )
        return user

    # Получить статистику по всем девайсам для пользователя по его id
    def get_device_stats_all_by_user_id(self, user_id: UUID, start_time: datetime, end_time: datetime):
        return self.device_stats_repository.get_device_stats_all_by_user_id(user_id, start_time, end_time)

    # Получить статистику по конкретному устройству для конкретного пользователя
    def get_current_device_stats_by_user_id(self, user_id: UUID, device_id: int, start_time: datetime, end_time: datetime):
        return self.device_stats_repository.get_current_device_stats_by_user_id(user_id, device_id, start_time, end_time)