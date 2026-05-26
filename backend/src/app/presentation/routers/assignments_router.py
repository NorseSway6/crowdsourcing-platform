from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.entities.response_schema import ErrorResponse


def get_assignments_router(assigment_handlers):
    router = Router(tags=["assignments"])

    def get_assignments_by_user(request, user_id: UUID) -> tuple[int, list[AssignmentOut] | ErrorResponse]:
        return assigment_handlers.get_assignments_by_user(request, user_id)

    router.add_api_operation(
        "/my",
        ["GET"],
        get_assignments_by_user,
        response={200: list[AssignmentOut], 404: ErrorResponse},
    )

    def create_assignment(request, user_id: UUID, pool_id: int) -> tuple[int, AssignmentOut | ErrorResponse]:
        return assigment_handlers.create_assignment(request, user_id, pool_id)

    router.add_api_operation(
        "/next",
        ["POST"],
        create_assignment,
        response={201: AssignmentOut, 400: ErrorResponse},
    )

    def update_assignment(
        request, user_id: UUID, assignment_id: int, data: AssignmentSchema
    ) -> tuple[int, AssignmentOut | ErrorResponse]:
        return assigment_handlers.update_assignment(request, user_id, assignment_id, data)

    router.add_api_operation(
        "/{int:assignment_id}",
        ["PATCH"],
        update_assignment,
        response={200: AssignmentOut, 400: ErrorResponse},
    )

    return router


def add_assignments_router(api: NinjaAPI, assignment_handlers):
    assignments_router = get_assignments_router(assignment_handlers)
    api.add_router("/assignments", assignments_router)
