from ninja import Body, NinjaAPI, Path, Query, Router

from app.domain.entities.pool_schema import PoolFilter, PoolOut, PoolSchema
from app.domain.entities.response_schema import ErrorResponse
from app.presentation.api.auth import customer_auth, student_auth
from app.presentation.api.handlers import PoolHandlers


def get_pools_router(pool_handlers: PoolHandlers):
    router = Router(tags=["pools"])

    def get_all_pools(request, filters: PoolFilter = Query(...)) -> tuple[int, list[PoolOut] | ErrorResponse]:
        return pool_handlers.get_all_pools(request, filters)

    router.add_api_operation(
        "/", ["GET"], get_all_pools, response={200: list[PoolOut], 404: ErrorResponse}, auth=student_auth
    )

    def get_pool_by_id(request, pool_id: int = Path(...)) -> tuple[int, PoolOut | ErrorResponse]:
        return pool_handlers.get_pool_by_id(request, pool_id)

    router.add_api_operation(
        "/{int:pool_id}",
        ["GET"],
        get_pool_by_id,
        response={200: PoolOut, 404: ErrorResponse},
        auth=[student_auth, customer_auth],
    )

    def update_pool(
        request, pool_id: int = Path(...), data: PoolSchema = Body(...)
    ) -> tuple[int, PoolOut | ErrorResponse]:
        return pool_handlers.update_pool(request, pool_id, data)

    router.add_api_operation(
        "/{int:pool_id}",
        ["PATCH"],
        update_pool,
        response={200: PoolOut, 400: ErrorResponse, 404: ErrorResponse},
        auth=customer_auth,
    )

    return router


def add_pools_router(api: NinjaAPI, pool_handlers: PoolHandlers):
    pools_router = get_pools_router(pool_handlers)
    api.add_router("/pools", pools_router)
