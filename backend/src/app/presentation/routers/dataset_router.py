from typing import List
from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.entities.error_response import ErrorResponse
from app.presentation.api.handlers import DatasetHandlers


def get_datasets_router(dataset_handlers: DatasetHandlers):
    router = Router(tags=["datasets"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: dataset_handlers.get_all_datasets(request),
        response={200: List[DatasetOut], 404: ErrorResponse},
    )

    def get_dataset_by_id(request, dataset_id: int) -> DatasetOut:
        return dataset_handlers.get_dataset_by_id(request, dataset_id)

    router.add_api_operation(
        "/{int:dataset_id}",
        ["GET"],
        get_dataset_by_id,
        response={200: DatasetOut, 404: ErrorResponse},
    )

    def create_dataset(request, owner_id: UUID, data: DatasetSchema) -> DatasetOut:
        return dataset_handlers.create_dataset(request, owner_id, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_dataset,
        response={200: DatasetOut},
    )

    def update_dataset(request, dataset_id: int, data: DatasetSchema) -> DatasetOut:
        return dataset_handlers.update_dataset(request, dataset_id, data)

    router.add_api_operation(
        "/{int:dataset_id}",
        ["PATCH"],
        update_dataset,
        response={200: DatasetOut, 404: ErrorResponse},
    )

    return router


def add_datasets_router(api: NinjaAPI, dataset_handlers: DatasetHandlers):
    datasets_router = get_datasets_router(dataset_handlers)
    api.add_router("/datasets", datasets_router)
