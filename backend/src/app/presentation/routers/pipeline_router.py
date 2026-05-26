from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.pipline_schema import PipelineOut, PipelineSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.presentation.api.handlers import PipelineHandlers


def get_pipelines_router(pipeline_handlers: PipelineHandlers):
    router = Router(tags=["pipelines"])

    def get_pipelines_by_user(request, owner_id: UUID) -> tuple[int, list[PipelineOut] | ErrorResponse]:
        return pipeline_handlers.get_pipelines_by_user(request, owner_id)

    router.add_api_operation(
        "/my",
        ["GET"],
        get_pipelines_by_user,
        response={200: list[PipelineOut], 404: ErrorResponse},
    )

    def create_pipeline(request, owner_id: UUID, data: PipelineSchema) -> tuple[int, PipelineOut | ErrorResponse]:
        return pipeline_handlers.create_pipeline(request, owner_id, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_pipeline,
        response={201: PipelineOut, 400: ErrorResponse},
    )

    def update_pipeline(request, pipeline_id: int, data: PipelineSchema) -> tuple[int, PipelineOut | ErrorResponse]:
        return pipeline_handlers.update_pipeline(request, pipeline_id, data)

    router.add_api_operation(
        "/{pipeline_id}",
        ["PATCH"],
        update_pipeline,
        response={200: PipelineOut, 400: ErrorResponse},
    )

    def delete_pipeline(request, pipeline_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        return pipeline_handlers.delete_pipeline(request, pipeline_id)

    router.add_api_operation(
        "/{pipeline_id}",
        ["DELETE"],
        delete_pipeline,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    return router


def add_pipelines_router(api: NinjaAPI, pipeline_handlers: PipelineHandlers):
    pipelines_router = get_pipelines_router(pipeline_handlers)
    api.add_router("/pipelines", pipelines_router)
