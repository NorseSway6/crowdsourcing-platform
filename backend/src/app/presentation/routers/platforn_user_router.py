from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.auth_roles import AuthRole, has_roles
from app.domain.entities.platform_user_schema import UserOut
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.user_profile_schema import ProfileSchema
from app.presentation.api.handlers import UserHandlers


def get_users_router(user_handlers: UserHandlers):
    router = Router(tags=["users"])

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def get_all_users(request):
        return user_handlers.get_all_users(request)

    router.add_api_operation(
        "/",
        ["GET"],
        get_all_users,
        response={200: list[UserOut], 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def get_user_by_id(request) -> tuple[int, UserOut | ErrorResponse]:
        user = request.auth
        return user_handlers.get_user_by_id(request, user.user_id)

    router.add_api_operation(
        "/me",
        ["GET"],
        get_user_by_id,
        response={200: UserOut, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def update_user_profile(request, data: ProfileSchema) -> tuple[int, UserOut | ErrorResponse]:
        user = request.auth
        return user_handlers.update_user_profile(request, user.user_id, data)

    router.add_api_operation(
        "/me/profile",
        ["PATCH"],
        update_user_profile,
        response={200: UserOut, 400: ErrorResponse, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def delete_user(request, user_id: UUID) -> tuple[int, SuccessResponse | ErrorResponse]:
        user = request.auth
        return user_handlers.delete_user(request, user.user_id)

    router.add_api_operation(
        "/",
        ["DELETE"],
        delete_user,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    return router


def add_users_router(api: NinjaAPI, user_handlers: UserHandlers):
    pools_router = get_users_router(user_handlers)
    api.add_router("/users", pools_router)
