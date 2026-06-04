from ninja import NinjaAPI, Router

from app.domain.entities.auth_schema import LogIn, RefreshTokenIn, TokenOut
from app.domain.entities.platform_user_schema import RegisterOut, RegisterSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.presentation.api.handlers import AuthHandlers


def get_auth_router(auth_handlers: AuthHandlers):
    router = Router(tags=["auth"])

    def create_tokens(request, data: LogIn) -> tuple[int, TokenOut | ErrorResponse]:
        return auth_handlers.create_tokens(request, data)

    router.add_api_operation(
        "/login",
        ["POST"],
        create_tokens,
        response={200: TokenOut, 400: ErrorResponse},
        auth=None,
    )

    def update_revoked_status(request, data: RefreshTokenIn) -> tuple[int, SuccessResponse | ErrorResponse]:
        return auth_handlers.update_revoked_status(request, data)

    router.add_api_operation(
        "/logout",
        ["POST"],
        update_revoked_status,
        response={200: SuccessResponse, 400: ErrorResponse},
        auth=None,
    )

    def update_token(request, data: RefreshTokenIn) -> tuple[int, TokenOut | ErrorResponse]:
        return auth_handlers.update_token(request, data)

    router.add_api_operation(
        "/update_tokens",
        ["POST"],
        update_token,
        response={200: TokenOut, 400: ErrorResponse},
        auth=None,
    )

    def register_user(request, data: RegisterSchema) -> tuple[int, RegisterOut | ErrorResponse]:
        return auth_handlers.register_user(request, data)

    router.add_api_operation(
        "/register", ["POST"], register_user, response={201: RegisterOut, 400: ErrorResponse}, auth=None
    )

    return router


def add_auth_router(api: NinjaAPI, auth_handlers: AuthHandlers):
    auth_router = get_auth_router(auth_handlers)
    api.add_router("/auth", auth_router)
