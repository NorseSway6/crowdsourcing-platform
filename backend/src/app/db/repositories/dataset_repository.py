from multiprocessing import Pool
from typing import List
from uuid import UUID

from app.db.models.dataset import Dataset
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.interfaces.datset_interface import IDatasetRepository


class DatasetRepository(IDatasetRepository):
    def get_all_datasets(self) -> List[DatasetOut]:
        return Dataset.objects.all()

    def get_dataset_by_id(self, dataset_id: int) -> DatasetOut:
        return Dataset.objects.filter(dataset_id=dataset_id).first()

    def create_dataset(self, owner_id: UUID, dataset_data: dict) -> DatasetOut:
        dataset = Dataset.objects.create(owner_id=owner_id, **dataset_data)
        return dataset

    def update_dataset(self, dataset_id: int, dataset_data: dict) -> DatasetOut:
        Dataset.objects.filter(dataset_id=dataset_id).update(**dataset_data)
        return Dataset.objects.get(dataset_id=dataset_id)
