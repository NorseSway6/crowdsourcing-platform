from uuid import UUID

from app.db.models.dataset import Dataset, DatasetCategory
from app.domain.entities.dataset_schema import CategorySchema, DatasetOut, DatasetSchema


class IDatasetRepository:
    def get_dataset_by_id(self, dataset_id: int) -> Dataset:
        pass

    def get_datasets_by_user(self, user_id: UUID) -> list[DatasetOut]:
        pass

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> Dataset:
        pass

    def get_categories_by_names(self, categories: list[str]) -> list[DatasetCategory]:
        pass

    def get_categories_by_dataset(self, dataset_id: int) -> list[DatasetCategory]:
        pass

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> bool:
        pass

    def delete_dataset(self, dataset_id: int) -> bool:
        pass

    def get_all_categories(self) -> list[DatasetCategory]:
        pass

    def create_category(self, category_data: CategorySchema) -> DatasetCategory:
        pass

    def delete_category(self, category_data: CategorySchema) -> bool:
        pass
