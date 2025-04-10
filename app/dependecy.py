from fastapi import Depends

from database import get_db_session
from repository import DeviceStatsRepository
from service import DeviceStatsService


def get_device_stats_repository() -> DeviceStatsRepository:
    db_session = get_db_session()
    return DeviceStatsRepository(db_session)


def get_device_stats_service(
    device_stats_repository: DeviceStatsRepository = Depends(get_device_stats_repository),
) -> DeviceStatsService:
    return DeviceStatsService(
        device_stats_repository=device_stats_repository,
    )

# Для Celery
def get_celery_device_stats_service() -> DeviceStatsService:
    db = get_db_session()
    try:
        repo = DeviceStatsRepository(db)
        return DeviceStatsService(repo)
    except Exception:
        db.close()
        raise