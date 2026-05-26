from ninja import NinjaAPI, Router

from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.presentation.api.handlers import PoolHandlers


def get_pools_router(pool_handlers: PoolHandlers):
    router = Router(tags=["pools"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: pool_handlers.get_all_pools(request),
        response={200: list[PoolOut], 404: ErrorResponse},
    )

    def get_pool_by_id(request, pool_id: int) -> tuple[int, PoolOut | ErrorResponse]:
        return pool_handlers.get_pool_by_id(request, pool_id)

    router.add_api_operation(
        "/{int:pool_id}",
        ["GET"],
        get_pool_by_id,
        response={200: PoolOut, 404: ErrorResponse},
    )

    def update_pool(request, pool_id: int, data: PoolSchema) -> tuple[int, PoolOut | ErrorResponse]:
        return pool_handlers.update_pool(request, pool_id, data)

    router.add_api_operation(
        "/{int:pool_id}",
        ["PATCH"],
        update_pool,
        response={200: PoolOut, 400: ErrorResponse},
    )

    return router


def add_pools_router(api: NinjaAPI, pool_handlers: PoolHandlers):
    pools_router = get_pools_router(pool_handlers)
    api.add_router("/pools", pools_router)
