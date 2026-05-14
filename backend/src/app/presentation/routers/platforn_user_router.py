from typing import List
from uuid import UUID

from ninja import NinjaAPI, Router

from app.domain.entities.platform_user_schema import UserOut, UserSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.user_profile_schema import ProfileSchema
from app.presentation.api.handlers import UserHandlers


def get_users_router(user_handlers: UserHandlers):
    router = Router(tags=["users"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: user_handlers.get_all_users(request),
        response={200: List[UserOut], 404: ErrorResponse},
    )

    def get_user_by_id(request, id: UUID) -> UserOut:
        return user_handlers.get_user_by_id(request, id)

    router.add_api_operation(
        "/me",
        ["GET"],
        get_user_by_id,
        response={200: UserOut, 404: ErrorResponse},
    )

    def create_user(request, data: UserSchema) -> UserOut:
        return user_handlers.create_user(request, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_user,
        response={201: UserOut, 404: ErrorResponse, 409: ErrorResponse},
    )

    def update_user_profile(request, id: UUID, data: ProfileSchema) -> UserOut:
        return user_handlers.update_user_profile(request, id, data)

    router.add_api_operation(
        "/me/profile",
        ["PATCH"],
        update_user_profile,
        response={200: UserOut, 404: ErrorResponse, 409: ErrorResponse},
    )

    def delete_user(request, id: UUID) -> bool:
        return user_handlers.delete_user(request, id)

    router.add_api_operation(
        "/",
        ["DELETE"],
        delete_user,
        response={200: SuccessResponse, 404: ErrorResponse},
    )

    return router


def add_users_router(api: NinjaAPI, user_handlers: UserHandlers):
    pools_router = get_users_router(user_handlers)
    api.add_router("/users", pools_router)
