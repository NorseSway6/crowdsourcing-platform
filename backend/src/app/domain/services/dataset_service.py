from uuid import UUID

from django.core.files.storage import default_storage
from django.db import transaction
from ninja import UploadedFile

import app.domain.exceptions as exc
from app.domain.entities.dataset_schema import CategoryOut, CategorySchema, DatasetOut, DatasetSchema
from app.domain.interfaces.datset_interface import IDatasetRepository
from app.domain.services.celery_tasks import process_images_upload_task, process_video_upload_task


class DatasetService:
    def __init__(self, dataset_repo: IDatasetRepository):
        self._dataset_repo = dataset_repo

    def get_dataset_by_id(self, dataset_id: int) -> DatasetOut:
        dataset = self._dataset_repo.get_dataset_by_id(dataset_id)
        if not dataset:
            raise exc.DatasetNotFoundError()
        return DatasetOut.from_orm(dataset)

    def get_datasets_by_user(self, user_id: UUID) -> list[DatasetOut]:
        datasets = self._dataset_repo.get_datasets_by_user(user_id)
        if not datasets:
            raise exc.DatasetNotFoundError()
        return [DatasetOut.from_orm(dataset) for dataset in datasets]

    def create_dataset(self, owner_id: UUID, dataset_data: DatasetSchema) -> DatasetOut:
        with transaction.atomic():
            dataset = self._dataset_repo.create_dataset(owner_id, dataset_data)
            if not dataset:
                raise exc.DatasetCreationFailedError()

            categories = dataset_data.categories
            if not categories:
                raise exc.CategoriesNotFoundError()

            category_names = list(set(dataset_data.categories))
            existing_categories = self._dataset_repo.get_categories_by_names(category_names)
            if not existing_categories or len(existing_categories) != len(category_names):
                raise exc.CategoriesNotFoundError()

            dataset.categories.add(*existing_categories)

            return DatasetOut.from_orm(dataset)

    def update_dataset(self, dataset_id: int, dataset_data: DatasetSchema) -> DatasetOut:
        updated = self._dataset_repo.update_dataset(dataset_id, dataset_data)
        if not updated:
            raise exc.DatasetUpdatingError()

        dataset = self._dataset_repo.get_dataset_by_id(dataset_id)
        return DatasetOut.from_orm(dataset)

    def delete_dataset(self, dataset_id: int) -> bool:
        deleted = self._dataset_repo.delete_dataset(dataset_id)
        if not deleted:
            raise exc.DatasetDeletionError()
        return deleted

    def upload_images(self, dataset_id: int, files: list[UploadedFile]) -> str:
        temp_file_paths = []

        for file in files:
            temp_path = f"temp_uploads/dataset_{dataset_id}/{file.name}"
            actual_saved_path = default_storage.save(temp_path, file)
            temp_file_paths.append((actual_saved_path, file.name))

        job = process_images_upload_task.delay(dataset_id, temp_file_paths)

        return job.id

    def upload_video(self, dataset_id: int, file: UploadedFile) -> str:
        temp_path = f"temp_uploads/video_{dataset_id}/{file.name}"
        actual_saved_path = default_storage.save(temp_path, file)
        temp_file_path = (actual_saved_path, file.name)

        job = process_video_upload_task.delay(dataset_id, temp_file_path)

        return job.id

    def get_all_categories(self) -> list[CategoryOut]:
        categories = self._dataset_repo.get_all_categories()
        if not categories:
            raise exc.CategoriesNotFoundError()
        return [CategoryOut.from_orm(c) for c in categories]

    def create_category(self, category_data: CategorySchema) -> CategoryOut:
        category = self._dataset_repo.create_category(category_data)
        if not category:
            raise exc.CreateCategoryError()
        return CategoryOut.from_orm(category)

    def delete_category(self, category_data: CategorySchema) -> bool:
        deleted = self._dataset_repo.delete_category(category_data)
        if not deleted:
            raise exc.DeleteCategorysError()
        return deleted
