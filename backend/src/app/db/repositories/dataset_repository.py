from multiprocessing import Pool
from typing import List
from uuid import UUID

from django.db import transaction
from ninja import UploadedFile
from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.dataset import Dataset
from app.db.models.task import Task
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.entities.task_schema import TaskOut
from app.domain.interfaces.datset_interface import IDatasetRepository


class DatasetRepository(IDatasetRepository):
    def get_all_datasets(self) -> List[DatasetOut]:
        datasets = Dataset.objects.all()
        if not datasets:
            raise HttpError(404, "Datasets not found")
        return [DatasetOut.from_orm(d) for d in datasets]

    def get_dataset_by_id(self, dataset_id: int) -> DatasetOut:
        dataset = Dataset.objects.filter(dataset_id=dataset_id).first()
        if dataset is None:
            raise HttpError(404, "Dataset not found")
        return DatasetOut.from_orm(dataset)

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> DatasetOut:
        try:
            dataset = Dataset.objects.create(owner_id=owner_id, name=dataset_data.name, domain=dataset_data.domain)
        except IntegrityError:
            raise HttpError(409, "Create failed due to integrity error")

        return DatasetOut.from_orm(dataset)

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> DatasetOut:
        dataset = Dataset.objects.filter(dataset_id=dataset_id).update(
            name=dataset_data.name, domain=dataset_data.domain
        )
        if dataset is None:
            raise HttpError(404, "Dataset not found")
        return Dataset.objects.get(dataset_id=dataset_id)

    def delete_dataset(self, dataset_id: int) -> bool:
        deleted, _ = Dataset.objects.filter(dataset_id=dataset_id).delete()
        if not deleted:
            raise HttpError(404, "Pool for delete not found")
        return deleted

    def upload_images(self, dataset_id: int, files: List[UploadedFile]) -> List[TaskOut]:
        tasks_to_create = []

        try:
            with transaction.atomic():
                for file in files:
                    task = Task(dataset_id=dataset_id)

                    try:
                        task.image.save(file.name, file, save=False)
                    except Exception:
                        raise HttpError(409, "Upload failed due to integrity error")

                    tasks_to_create.append(task)

                created_tasks = Task.objects.bulk_create(tasks_to_create)
        except IntegrityError:
            raise HttpError(409, "Upload failed due to integrity error")

        return [TaskOut.from_orm(t) for t in created_tasks]
