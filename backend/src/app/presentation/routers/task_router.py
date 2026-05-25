from typing import List
from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.task_schema import TaskOut
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

    def delete_task(request, task_id: int) -> bool:
        return task_handlers.delete_task(request, task_id)

    router.add_api_operation(
        "/{int:task_id}",
        ["DELETE"],
        delete_task,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    return router


def add_tasks_router(api: NinjaAPI, task_handlers: TaskHandlers):
    task_router = get_tasks_router(task_handlers)
    api.add_router("/tasks", task_router)
