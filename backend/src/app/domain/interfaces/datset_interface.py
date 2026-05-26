from uuid import UUID

from ninja import UploadedFile

from app.db.models.dataset import Dataset
from app.db.models.task import Task
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema


class IDatasetRepository:
    def get_dataset_by_id(self, dataset_id: int) -> Dataset:
        pass

    def get_datasets_by_user(self, user_id: UUID) -> list[DatasetOut]:
        pass

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> Dataset:
        pass

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> Dataset:
        pass

    def delete_dataset(self, dataset_id: int) -> bool:
        pass

    def upload_images(self, dataset_id: int, files: list[UploadedFile]) -> list[Task]:
        pass
