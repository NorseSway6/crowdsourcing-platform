from typing import List

from ninja import NinjaAPI, Router

from app.domain.entities.error_response import ErrorResponse
from app.domain.entities.pool_schema import PoolOut
from app.presentation.api.handlers import PoolHandlers


def get_pools_router(pool_handlers: PoolHandlers):
    router = Router(tags=["pools"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: pool_handlers.get_all_pools(request),
        response={200: List[PoolOut], 404: ErrorResponse},
    )

    return router


def add_pools_router(api: NinjaAPI, pool_handlers: PoolHandlers):
    pools_router = get_pools_router(pool_handlers)
    api.add_router("/pools", pools_router)
