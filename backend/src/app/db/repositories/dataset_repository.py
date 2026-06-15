from uuid import UUID

from django.core.cache import cache
from django.db import IntegrityError

from app.db.models.dataset import Dataset, DatasetCategory
from app.db.models.task import Task
from app.domain.entities.dataset_schema import CategorySchema, DatasetOut, DatasetSchema
from app.domain.interfaces.datset_interface import IDatasetRepository
from config import settings


class DatasetRepository(IDatasetRepository):
    CACHE_KEY = "all_categories_list"

    def get_dataset_by_id(self, dataset_id: int) -> Dataset:
        return Dataset.objects.filter(dataset_id=dataset_id).first()

    def get_datasets_by_user(self, user_id: UUID) -> list[DatasetOut]:
        return list(Dataset.objects.filter(owner_id=user_id))

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> Dataset:
        try:
            dataset = Dataset.objects.create(owner_id=owner_id, name=dataset_data.name, domain=dataset_data.domain)
        except IntegrityError:
            return None

        return dataset

    def get_categories_by_names(self, categories: list[str]) -> list[DatasetCategory]:
        return list(DatasetCategory.objects.filter(name__in=categories))

    def get_categories_by_dataset(self, dataset_id: int) -> list[DatasetCategory]:
        return list(DatasetCategory.objects.filter(dataset_category__dataset_id=dataset_id))

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> bool:
        return Dataset.objects.filter(dataset_id=dataset_id).update(name=dataset_data.name, domain=dataset_data.domain)

    def delete_dataset(self, dataset_id: int) -> bool:
        deleted, _ = Dataset.objects.filter(dataset_id=dataset_id).delete()
        return deleted > 0

    def get_all_categories(self) -> list[DatasetCategory]:
        cached_categories = cache.get(self.CACHE_KEY)
        if cached_categories:
            return cached_categories

        categories = list(DatasetCategory.objects.all())

        cache.set(self.CACHE_KEY, categories, settings.CACHE_TIMEOUT)

        return categories

    def create_category(self, category_data: CategorySchema) -> DatasetCategory:
        try:
            category, created = DatasetCategory.objects.get_or_create(name=category_data.name)

            if created:
                cache.delete(self.CACHE_KEY)
        except IntegrityError:
            return None

        return category

    def delete_category(self, category_data: CategorySchema) -> bool:
        deleted, _ = DatasetCategory.objects.filter(name=category_data.name).delete()

        if deleted > 0:
            cache.delete(self.CACHE_KEY)
        return deleted > 0
