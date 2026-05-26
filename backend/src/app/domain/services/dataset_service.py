from uuid import UUID

from ninja import UploadedFile

from app.db.repositories.dataset_repository import DatasetRepository
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.entities.task_schema import TaskOut


class DatasetService:
    def __init__(self, dataset_repo: DatasetRepository):
        self._dataset_repo = dataset_repo

    def get_dataset_by_id(self, dataset_id: int) -> DatasetOut:
        dataset = self._dataset_repo.get_dataset_by_id(dataset_id)
        if not dataset:
            return None
        return DatasetOut.from_orm(dataset)

    def get_datasets_by_user(self, user_id: UUID) -> list[DatasetOut]:
        datasets = self._dataset_repo.get_datasets_by_user(user_id)
        if not datasets:
            return None
        return DatasetOut.from_orm(datasets)

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> DatasetOut:
        dataset = self._dataset_repo.create_dataset(owner_id, dataset_data)
        if not dataset:
            return None
        return DatasetOut.from_orm(dataset)

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> DatasetOut:
        updated = self._dataset_repo.update_dataset(dataset_id, dataset_data)
        if not updated:
            return None
        return DatasetOut.from_orm(updated)

    def delete_dataset(self, dataset_id: int) -> bool:
        deleted = self._dataset_repo.delete_dataset(dataset_id)
        if not deleted:
            return None
        return deleted

    def upload_images(self, dataset_id: int, files: list[UploadedFile]) -> list[TaskOut]:
        images = self._dataset_repo.upload_images(dataset_id, files)
        if not images:
            return None
        return [TaskOut.from_orm(image) for image in images]
