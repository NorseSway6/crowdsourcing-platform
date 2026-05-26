from uuid import UUID

from django.db import IntegrityError, transaction
from ninja import UploadedFile

from app.db.models.dataset import Dataset
from app.db.models.task import Task
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.interfaces.datset_interface import IDatasetRepository


class DatasetRepository(IDatasetRepository):
    def get_dataset_by_id(self, dataset_id: int) -> Dataset:
        return Dataset.objects.filter(dataset_id=dataset_id).first()

    def get_datasets_by_user(self, user_id: UUID) -> list[DatasetOut]:
        return Dataset.objects.filter(owner_id=user_id)

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> Dataset:
        try:
            dataset = Dataset.objects.create(owner_id=owner_id, name=dataset_data.name, domain=dataset_data.domain)
        except IntegrityError:
            return None

        return dataset

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> bool:
        return Dataset.objects.filter(dataset_id=dataset_id).update(name=dataset_data.name, domain=dataset_data.domain)

    def delete_dataset(self, dataset_id: int) -> bool:
        deleted, _ = Dataset.objects.filter(dataset_id=dataset_id).delete()
        return deleted > 0

    def upload_images(self, dataset_id: int, files: list[UploadedFile]) -> list[Task]:
        tasks_to_create = []

        try:
            with transaction.atomic():
                for file in files:
                    task = Task(dataset_id=dataset_id)

                    try:
                        task.image.save(file.name, file, save=False)
                    except Exception:
                        return None

                    tasks_to_create.append(task)

                created_tasks = Task.objects.bulk_create(tasks_to_create)
        except IntegrityError:
            return None

        return list(created_tasks)
