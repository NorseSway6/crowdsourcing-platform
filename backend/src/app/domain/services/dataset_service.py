from typing import List
from uuid import UUID

from ninja import UploadedFile

from app.db.repositories.dataset_repository import DatasetRepository
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.entities.task_schema import TaskOut


class DatasetService:
    def __init__(self, dataset_repo: DatasetRepository):
        self._dataset_repo = dataset_repo

    def get_all_datasets(self) -> List[DatasetOut]:
        return self._dataset_repo.get_all_datasets()

    def get_dataset_by_id(self, dataset_id: int) -> DatasetOut:
        return self._dataset_repo.get_dataset_by_id(dataset_id)

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> DatasetOut:
        return self._dataset_repo.create_dataset(owner_id, dataset_data)

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> DatasetOut:
        return self._dataset_repo.update_dataset(dataset_id, dataset_data)

    def delete_dataset(self, dataset_id: int) -> bool:
        return self._dataset_repo.delete_dataset(dataset_id)

    def upload_images(self, dataset_id: int, files: List[UploadedFile]) -> List[TaskOut]:
        return self._dataset_repo.upload_images(dataset_id, files)
