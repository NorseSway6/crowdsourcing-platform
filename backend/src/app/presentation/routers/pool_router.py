from typing import List

from ninja import NinjaAPI, Router

from app.domain.entities.pool_schema import PoolIn, PoolOut, PoolSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.presentation.api.handlers import PoolHandlers


def get_pools_router(pool_handlers: PoolHandlers):
    router = Router(tags=["pools"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: pool_handlers.get_all_pools(request),
        response={200: List[PoolOut], 404: ErrorResponse},
    )

    def get_pool_by_id(request, pool_id: int) -> PoolOut:
        return pool_handlers.get_pool_by_id(request, pool_id)

    router.add_api_operation(
        "/{int:pool_id}",
        ["GET"],
        get_pool_by_id,
        response={200: PoolOut, 404: ErrorResponse},
    )

    def create_pool(request, data: PoolIn) -> PoolOut:
        return pool_handlers.create_pool(request, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_pool,
        response={201: PoolOut, 400: ErrorResponse, 409: ErrorResponse},
    )

    def update_pool(request, pool_id: int, data: PoolSchema) -> PoolOut:
        return pool_handlers.update_pool(request, pool_id, data)

    router.add_api_operation(
        "/{int:pool_id}",
        ["PATCH"],
        update_pool,
        response={200: PoolOut, 404: ErrorResponse},
    )

    def delete_pool(request, pool_id: int) -> bool:
        return pool_handlers.delete_pool(request, pool_id)

    router.add_api_operation(
        "/{int:pool_id}",
        ["DELETE"],
        delete_pool,
        response={200: SuccessResponse, 404: ErrorResponse},
    )

    return router


def add_pools_router(api: NinjaAPI, pool_handlers: PoolHandlers):
    pools_router = get_pools_router(pool_handlers)
    api.add_router("/pools", pools_router)
