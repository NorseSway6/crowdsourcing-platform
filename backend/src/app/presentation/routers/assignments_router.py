from ninja import NinjaAPI, Router

from app.domain.auth_roles import AuthRole, has_roles
from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.entities.response_schema import ErrorResponse
from app.presentation.api.handlers import AssignmentHandlers


def get_assignments_router(assigment_handlers: AssignmentHandlers):
    router = Router(tags=["assignments"])

    @has_roles(AuthRole.ADMIN, AuthRole.STUDENT)
    def get_assignments_by_user(request) -> tuple[int, list[AssignmentOut] | ErrorResponse]:
        user = request.auth
        return assigment_handlers.get_assignments_by_user(request, user.user_id)

    router.add_api_operation(
        "/my",
        ["GET"],
        get_assignments_by_user,
        response={200: list[AssignmentOut], 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.STUDENT)
    def get_completed_assignments_by_user(request) -> tuple[int, list[AssignmentOut] | ErrorResponse]:
        user = request.auth
        return assigment_handlers.get_completed_assignments_by_user(request, user.user_id)

    router.add_api_operation(
        "/my/completed",
        ["GET"],
        get_completed_assignments_by_user,
        response={200: list[AssignmentOut], 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.STUDENT)
    def create_assignment(request, pool_id: int) -> tuple[int, AssignmentOut | ErrorResponse]:
        user = request.auth
        return assigment_handlers.create_assignment(request, user.user_id, pool_id)

    router.add_api_operation(
        "/next",
        ["POST"],
        create_assignment,
        response={201: AssignmentOut, 400: ErrorResponse, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.STUDENT)
    def update_assignment(
        request, assignment_id: int, data: AssignmentSchema
    ) -> tuple[int, AssignmentOut | ErrorResponse]:
        user = request.auth
        return assigment_handlers.update_assignment(request, user.user_id, assignment_id, data)

    router.add_api_operation(
        "/{int:assignment_id}",
        ["PATCH"],
        update_assignment,
        response={200: AssignmentOut, 400: ErrorResponse, 404: ErrorResponse},
    )

    return router


def add_assignments_router(api: NinjaAPI, assignment_handlers):
    assignments_router = get_assignments_router(assignment_handlers)
    api.add_router("/assignments", assignments_router)
