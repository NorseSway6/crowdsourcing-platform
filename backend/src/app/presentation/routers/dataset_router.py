from uuid import UUID

from ninja import NinjaAPI, Router, UploadedFile

from app.domain.entities.dataset_schema import CategoryOut, CategorySchema, DatasetOut, DatasetSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.task_schema import TaskOut
from app.presentation.api.auth import admin_auth, customer_auth
from app.presentation.api.handlers import DatasetHandlers


def get_datasets_router(dataset_handlers: DatasetHandlers):
    router = Router(tags=["datasets"])

    def get_dataset_by_id(request, dataset_id: int) -> tuple[int, DatasetOut | ErrorResponse]:
        return dataset_handlers.get_dataset_by_id(request, dataset_id)

    router.add_api_operation(
        "/{int:dataset_id}",
        ["GET"],
        get_dataset_by_id,
        response={200: DatasetOut, 404: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def get_datasets_by_user(request) -> tuple[int, list[DatasetOut] | ErrorResponse]:
        user = request.auth
        return dataset_handlers.get_datasets_by_user(request, user.user_id)

    router.add_api_operation(
        "/my",
        ["GET"],
        get_datasets_by_user,
        response={200: list[DatasetOut], 404: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def create_dataset(request, data: DatasetSchema) -> tuple[int, DatasetOut | ErrorResponse]:
        user = request.auth
        return dataset_handlers.create_dataset(request, user.user_id, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_dataset,
        response={201: DatasetOut, 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def upload_images(request, dataset_id: int, files: list[UploadedFile]) -> tuple[int, list[TaskOut] | ErrorResponse]:
        return dataset_handlers.upload_images(request, dataset_id, files)

    router.add_api_operation(
        "/{int:dataset_id}/upload",
        ["POST"],
        upload_images,
        response={201: list[TaskOut], 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def export_dataset(request, dataset_id: int, format_type: str) -> tuple[int, SuccessResponse | ErrorResponse]:
        return dataset_handlers.export_dataset(request, dataset_id, format_type)

    router.add_api_operation(
        "/{int:dataset_id}/export",
        ["GET"],
        export_dataset,
        response={200: None, 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def update_dataset(request, dataset_id: int, data: DatasetSchema) -> tuple[int, DatasetOut | ErrorResponse]:
        return dataset_handlers.update_dataset(request, dataset_id, data)

    router.add_api_operation(
        "/{int:dataset_id}",
        ["PATCH"],
        update_dataset,
        response={200: DatasetOut, 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def delete_dataset(request, dataset_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        return dataset_handlers.delete_dataset(request, dataset_id)

    router.add_api_operation(
        "/{int:dataset_id}",
        ["DELETE"],
        delete_dataset,
        response={200: SuccessResponse, 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    router.add_api_operation(
        "/categories",
        ["GET"],
        lambda request: dataset_handlers.get_all_categories(request),
        response={200: list[CategoryOut], 404: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def create_category(request, data: CategorySchema) -> CategoryOut:
        return dataset_handlers.create_category(request, data)

    router.add_api_operation(
        "/categories",
        ["POST"],
        create_category,
        response={201: CategoryOut, 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    def delete_category(request, data: CategorySchema) -> CategoryOut:
        return dataset_handlers.delete_category(request, data)

    router.add_api_operation(
        "/categories",
        ["DELETE"],
        delete_category,
        response={200: SuccessResponse, 400: ErrorResponse},
        auth=[customer_auth, admin_auth],
    )

    return router


def add_datasets_router(api: NinjaAPI, dataset_handlers: DatasetHandlers):
    datasets_router = get_datasets_router(dataset_handlers)
    api.add_router("/datasets", datasets_router)
