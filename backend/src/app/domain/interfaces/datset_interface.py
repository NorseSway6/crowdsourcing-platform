from typing import Dict, List
from uuid import UUID

from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema


class IDatasetRepository:
    def get_all_datasets(self) -> List[DatasetOut]:
        pass

    def get_dataset_by_id(self, dataset_id: int) -> DatasetOut:
        pass

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> DatasetOut:
        pass

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> DatasetOut:
        pass

    def delete_dataset(self, dataset_id: int) -> bool:
        pass
