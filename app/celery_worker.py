import os
import time
from datetime import datetime

from celery import Celery
from dotenv import load_dotenv

from dependecy import get_celery_device_stats_service
from uuid import UUID

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

@celery.task(name="get_device_stats_by_device_id")
def get_device_stats_by_device_id(device_id: int,
                start_time: datetime,
                end_time: datetime):

    service = get_celery_device_stats_service()
    result = service.get_device_stats_by_device_id(device_id, start_time, end_time)

    # Имитация задержки
    #time.sleep(10)
    return result


@celery.task(name="get_device_stats_all_by_user_id")
def get_device_stats_all_by_user_id(user_id: UUID,
                                  start_time: datetime,
                                  end_time: datetime):

    service = get_celery_device_stats_service()
    result = service.get_device_stats_all_by_user_id(user_id, start_time, end_time)

    # Имитация задержки
    #time.sleep(10)
    return result

@celery.task(name="get_current_device_stats_by_user_id")
def get_current_device_stats_by_user_id(user_id: UUID,
                                        device_id: int,
                                        start_time: datetime,
                                        end_time: datetime):
    service = get_celery_device_stats_service()
    result = service.get_current_device_stats_by_user_id(user_id, device_id, start_time, end_time)

    # Имитация задержки
    #time.sleep(10)
    return result

