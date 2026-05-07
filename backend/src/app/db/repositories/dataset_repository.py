from multiprocessing import Pool
from typing import List
from uuid import UUID

from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.dataset import Dataset
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
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
