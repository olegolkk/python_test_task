import time

from celery.worker.consumer.delayed_delivery import MAX_RETRIES

from locust import HttpUser, task, between
import uuid
import random
from datetime import datetime, timedelta


USER_IDS = [
    uuid.UUID("0ccd9927-7b6e-42e7-8f0b-b9bc0d03e32b"),
    uuid.UUID("eb5012ea-9c2d-4a20-908c-63ae4cf67b62"),
    uuid.UUID("f26a3045-bbfb-4f57-adfb-09f31a80e9ea"),
]

MAX_RETRIES = 5
class DeviceStatsUser(HttpUser):
    wait_time = between(0.5, 2)  # Пауза между запросами

    @task(3)
    def get_stats_by_device_id(self):
        device_id = random.randint(1, 10)
        with self.client.get(
                f"/api/devices/stats/{device_id}",
                name="/api/devices/stats/{device_id}",  # Группировка по шаблону
                catch_response=True
        ) as response:
            if not response.ok:
                response.failure("Failed to start task")
                return
            task_id = response.json()
            self._check_task_result(task_id)

    @task(3)
    def get_stats_all_by_user_id(self):
        user_id = random.choice(USER_IDS)
        with self.client.get(
                f"/api/devices/stats/{user_id}/all",
                name="/api/devices/stats/{user_id}/all",  # Группировка
                catch_response=True
        ) as response:
            if not response.ok:
                response.failure("Failed to start task")
                return
            task_id = response.json()
            self._check_task_result(task_id)

    @task(3)
    def get_stats_device_id_by_user_id(self):
        user_id = random.choice(USER_IDS)
        device_id = random.randint(1, 10)
        with self.client.get(
                f"/api/devices/stats/{user_id}/{device_id}",
                name="/api/devices/stats/{user_id}/{device_id}",  # Группировка
                catch_response=True
        ) as response:
            if not response.ok:
                response.failure("Failed to start task")
                return
            task_id = response.json()
            self._check_task_result(task_id)

    def _check_task_result(self, task_id):
        """Проверяем статус задачи через /task/{task_id}"""
        for _ in range(MAX_RETRIES):
            with self.client.get(
                    f"/api/tasks/{task_id}",
                    name="/api/tasks/{task_id}",
                    catch_response=True
            ) as task_response:
                if not task_response.ok:
                    task_response.failure(f"Task check failed: {task_id}")
                    return

                data = task_response.json()
                if data["status"] == "SUCCESS":
                    task_response.success()
                    return
                elif data["status"] == "FAILURE":
                    task_response.failure(f"Task failed: {data['error']}")
                    return

            # Если задача еще не завершена, ждем и пробуем снова
            time.sleep(1)  # Пауза перед повторной проверкой

        # Если исчерпали попытки
        raise Exception(f"Task {task_id} did not complete after {MAX_RETRIES} retries")