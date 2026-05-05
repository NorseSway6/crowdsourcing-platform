from typing import List
from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.error_response import ErrorResponse
from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.presentation.api.handlers import TaskHandlers


def get_tasks_router(task_handlers: TaskHandlers):
    router = Router(tags=["tasks"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: task_handlers.get_all_tasks(request),
        response={200: List[TaskOut], 404: ErrorResponse},
    )

    def get_task_by_id(request, task_id: int) -> TaskOut:
        return task_handlers.get_task_by_id(request, task_id)

    router.add_api_operation(
        "/{int:task_id}",
        ["GET"],
        get_task_by_id,
        response={200: TaskOut, 404: ErrorResponse},
    )

    def create_task(request, pool_id: int, user_id: UUID, data: TaskSchema) -> TaskOut:
        return task_handlers.create_task(request, pool_id, user_id, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_task,
        response={200: TaskOut},
    )

    return router


def add_tasks_router(api: NinjaAPI, task_handlers: TaskHandlers):
    task_router = get_tasks_router(task_handlers)
    api.add_router("/tasks", task_router)
