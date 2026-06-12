from ninja import NinjaAPI, Query, Router

from app.domain.auth_roles import AuthRole, has_roles
from app.domain.entities.anallytics_schema import PoolProgressOut, PoolsProgressFilter, UserInfoFilter, UserInfoOut
from app.domain.entities.response_schema import ErrorResponse
from app.presentation.api.handlers import AnalyticsHandlers


def get_analytics_router(analytics_handlers: AnalyticsHandlers):
    router = Router(tags=["analytics"])

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER)
    def get_pools_progress(request, filters: PoolsProgressFilter = Query(...)) -> list[PoolProgressOut]:
        user = request.auth
        return analytics_handlers.get_pools_progress(request, user.user_id, filters)

    router.add_api_operation(
        "/pools-progress",
        ["GET"],
        get_pools_progress,
        response={200: list[PoolProgressOut], 404: ErrorResponse},
    )

    def get_users_info(request, filters: UserInfoFilter = Query(...)) -> list[UserInfoOut]:
        return analytics_handlers.get_users_info(request, filters)

    router.add_api_operation(
        "/user-info",
        ["GET"],
        get_users_info,
        response={200: list[UserInfoOut], 404: ErrorResponse},
    )

    return router


def add_analytics_router(api: NinjaAPI, analytics_handlers):
    analytics_router = get_analytics_router(analytics_handlers)
    api.add_router("/analytics", analytics_router)
