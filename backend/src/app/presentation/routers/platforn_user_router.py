from typing import List
from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.error_response import ErrorResponse
from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.entities.user_profile_schema import ProfileSchema
from app.presentation.api.handlers import UserHandlers


def get_users_router(user_handlers: UserHandlers):
    router = Router(tags=["users"])

    def create_user(request, data: UserIn) -> UserOut:
        return user_handlers.get_or_create_user(request, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_user,
        response={201: UserOut},
    )

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: user_handlers.get_all_users(request),
        response={200: List[UserOut], 404: ErrorResponse},
    )

    # доступен только с авторизацией (будет позже), передача id временно
    def get_user_by_id(request, data: UUID) -> UserOut:
        return user_handlers.get_user_by_id(request, data)

    router.add_api_operation(
        "/me",
        ["GET"],
        get_user_by_id,
        response={200: UserOut, 401: ErrorResponse},
    )

    # доступен только с авторизацией (будет позже), передача id временно
    def update_user_profile(request, id: UUID, data: ProfileSchema) -> UserOut:
        return user_handlers.update_user_profile(request, id, data)

    router.add_api_operation(
        "/me/profile",
        ["PATCH"],
        update_user_profile,
        response={200: UserOut, 404: ErrorResponse},
    )

    return router


def add_users_router(api: NinjaAPI, user_handlers: UserHandlers):
    pools_router = get_users_router(user_handlers)
    api.add_router("/users", pools_router)
