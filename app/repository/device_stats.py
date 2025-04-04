from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from database import DeviceStats, User
from schemas import DeviceStatsCreateSchema, DeviceStatsResponseSchema, UserResponseSchema, UserCreateSchema


class DeviceStatsRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_device_stats(self, device_stats: DeviceStatsCreateSchema) -> UUID:
        device_stats_model = DeviceStats(**device_stats.dict())

        with self.db_session() as session:
            session.add(device_stats_model)
            session.commit()
            return device_stats_model.id

    # Получить статистику по конкретному девайсу
    def get_device_stats_by_device_id(self, device_id: int, start_time: datetime, end_time: datetime) -> dict:

        with self.db_session() as session:
            device_exists = session.query(
                session.query(DeviceStats).filter(DeviceStats.device_id == device_id).exists()
            ).scalar()

            if not device_exists:
                return {"error": f"Устройства с таким {device_id} не найдено"}, 404

            query = session.query(DeviceStats).filter(
                DeviceStats.device_id == device_id
            )

            if start_time:
                query = query.filter(DeviceStats.timestamp >= start_time)
            if end_time:
                query = query.filter(DeviceStats.timestamp <= end_time)

            subquery = query.subquery()

            # Для каждого параметра вычисляем статистику
            stats = {}
            for param in ['x', 'y', 'z']:
                stats[param] = {
                    'min': session.query(func.min(getattr(subquery.c, param))).scalar(),
                    'max': session.query(func.max(getattr(subquery.c, param))).scalar(),
                    'count': session.query(func.count(getattr(subquery.c, param))).scalar(),
                    'sum': session.query(func.sum(getattr(subquery.c, param))).scalar(),
                    'avg': session.query(func.avg(getattr(subquery.c, param))).scalar(),
                    'median': session.query(
                        func.percentile_cont(0.5).within_group(getattr(subquery.c, param).asc())
                    ).scalar()
                }

            return stats

    # Получить статистику по уникальному идентификатору статистики для девайся
    def get_device_stats_by_id(self, id: UUID) -> DeviceStatsResponseSchema:
        with self.db_session() as session:
            device_stats: DeviceStatsResponseSchema = session.execute(select(DeviceStats).where(DeviceStats.id == id)).scalar_one_or_none()
            return device_stats

    # Создать пользователя
    def create_user(self, user: UserCreateSchema) -> UUID:
        user_model = User(**user.dict())
        with self.db_session() as session:
            session.add(user_model)
            session.commit()
            return user_model.id

    # Получить пользователя по id
    def get_user_by_id(self, user_id: UUID) -> UserResponseSchema:
        with self.db_session() as session:
            user: UserResponseSchema = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
            return user

    def get_user_by_email(self, email: str) -> UserResponseSchema:
        with self.db_session() as session:
            user: UserResponseSchema = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
            return user

    # Получить статистику для пользователя обо всех устройствах
    def get_device_stats_all_by_user_id(self, user_id: UUID, start_time: datetime, end_time: datetime):
        with self.db_session() as session:
            # Базовый запрос с фильтрами по пользователю и времени
            query = session.query(DeviceStats).filter(
                DeviceStats.user_id == user_id
            )

            if start_time:
                query = query.filter(DeviceStats.timestamp >= start_time)
            if end_time:
                query = query.filter(DeviceStats.timestamp <= end_time)

            # Группируем по device_id и вычисляем статистику для каждого устройства
            device_stats = {}

            # Получаем список уникальных device_id для пользователя
            device_ids = [id for (id,) in session.query(DeviceStats.device_id).filter(
                DeviceStats.user_id == user_id
            ).distinct().all()]

            for device_id in device_ids:
                # Фильтруем записи по конкретному device_id
                device_query = query.filter(DeviceStats.device_id == device_id)

                stats = {}
                for param in ['x', 'y', 'z']:
                    stats[param] = {
                        'min': device_query.with_entities(func.min(getattr(DeviceStats, param))).scalar(),
                        'max': device_query.with_entities(func.max(getattr(DeviceStats, param))).scalar(),
                        'count': device_query.with_entities(func.count(getattr(DeviceStats, param))).scalar(),
                        'sum': device_query.with_entities(func.sum(getattr(DeviceStats, param))).scalar(),
                        'avg': device_query.with_entities(func.avg(getattr(DeviceStats, param))).scalar(),
                        'median': session.query(
                            func.percentile_cont(0.5).within_group(getattr(DeviceStats, param).asc())
                        ).filter(
                            DeviceStats.user_id == user_id,
                            DeviceStats.device_id == device_id,
                            *([DeviceStats.timestamp >= start_time] if start_time else []),
                            *([DeviceStats.timestamp <= end_time] if end_time else [])
                        ).scalar()
                    }

                device_stats[device_id] = stats

            return device_stats

    # Получить статистику для пользователя обо всех устройствах
    def get_current_device_stats_by_user_id(self, user_id: UUID, device_id: int, start_time: datetime, end_time: datetime):
        with self.db_session() as session:
            device_exists = session.query(
                session.query(DeviceStats).filter(DeviceStats.device_id == device_id).exists()
            ).scalar()

            if not device_exists:
                return {"error": f"Устройства с таким {device_id} не найдено"}, 404

            query = session.query(DeviceStats).filter(
                DeviceStats.user_id == user_id,
                DeviceStats.device_id == device_id
            )

            if start_time:
                query = query.filter(DeviceStats.timestamp >= start_time)
            if end_time:
                query = query.filter(DeviceStats.timestamp <= end_time)

            subquery = query.subquery()

            # Для каждого параметра вычисляем статистику
            stats = {}
            for param in ['x', 'y', 'z']:
                stats[param] = {
                    'min': session.query(func.min(getattr(subquery.c, param))).scalar(),
                    'max': session.query(func.max(getattr(subquery.c, param))).scalar(),
                    'count': session.query(func.count(getattr(subquery.c, param))).scalar(),
                    'sum': session.query(func.sum(getattr(subquery.c, param))).scalar(),
                    'avg': session.query(func.avg(getattr(subquery.c, param))).scalar(),
                    'median': session.query(
                        func.percentile_cont(0.5).within_group(getattr(subquery.c, param).asc())
                    ).scalar()
                }

            return stats

