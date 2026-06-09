import logging

from celery import current_task, shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django_redis import get_redis_connection
from PIL import Image

import app.domain.exceptions as exc
from app.db.models.task import Task
from app.db.repositories.dataset_repository import DatasetRepository
from app.db.repositories.task_repository import TaskRepository
from app.domain.services.export_service import ExportService


@shared_task(bind=True)
def run_dataset_export_task(self, dataset_id: int, format_type: str) -> str:
    lock_key = f"export_lock:dataset:{dataset_id}"  # noqa: E231
    redis_client = get_redis_connection("default")

    try:
        task_repo = TaskRepository()
        dataset_repo = DatasetRepository()
        export_service = ExportService(export_repo=task_repo, dataset_repo=dataset_repo)

        file_bytes = export_service.execute(dataset_id, format_type)

        if not file_bytes:
            raise exc.EmptyExportData()

        job_id = self.request.id if self.request else current_task.request.id
        filename = f"exports/dataset_{dataset_id}_{job_id}.json"

        saved_path = default_storage.save(filename, ContentFile(file_bytes))

        download_url = default_storage.url(saved_path)

        return download_url

    except Exception:
        raise exc.ExportDatasetError()

    finally:
        redis_client.delete(lock_key)


@shared_task
def process_images_upload_task(dataset_id: int, temp_files: list[list[str]]) -> int:
    tasks_to_create = []

    for s3_path, original_name in temp_files:
        try:
            task_repo = TaskRepository()
            with default_storage.open(s3_path, "rb") as f:
                with Image.open(f) as img:
                    width, height = img.size

                f.seek(0)
                file_bytes = f.read()

            task = Task(dataset_id=dataset_id, width=width, height=height)

            task.image.save(original_name, ContentFile(file_bytes), save=False)
            tasks_to_create.append(task)

            default_storage.delete(s3_path)

        except Exception:
            if default_storage.exists(s3_path):
                default_storage.delete(s3_path)
            continue

    if tasks_to_create:
        try:
            with transaction.atomic():
                task_repo.bulk_cerate_task(tasks_to_create)
            return len(tasks_to_create)
        except Exception:
            raise exc.UploadImageError()
    return 0
