from ninja import Body, NinjaAPI, Path, Query, Router

from app.domain.auth_roles import AuthRole, has_roles
from app.domain.entities.pool_schema import (
    PoolDetailOut,
    PoolFilter,
    PoolInstructionOut,
    PoolInstructionSchema,
    PoolOut,
    PoolSchema,
    PoolType,
)
from app.domain.entities.response_schema import ErrorResponse
from app.presentation.api.handlers import PoolHandlers


def get_pools_router(pool_handlers: PoolHandlers):
    router = Router(tags=["pools"])

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def get_all_pools(request, filters: PoolFilter = Query(...)) -> tuple[int, list[PoolOut] | ErrorResponse]:
        return pool_handlers.get_all_pools(request, filters)

    router.add_api_operation(
        "/",
        ["GET"],
        get_all_pools,
        response={200: list[PoolOut], 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def get_pool_by_id(request, pool_id: int = Path(...)) -> tuple[int, PoolOut | ErrorResponse]:
        return pool_handlers.get_pool_by_id(request, pool_id)

    router.add_api_operation(
        "/{int:pool_id}",
        ["GET"],
        get_pool_by_id,
        response={200: PoolOut, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER)
    def update_pool(
        request, pool_id: int = Path(...), data: PoolSchema = Body(...)
    ) -> tuple[int, PoolOut | ErrorResponse]:
        return pool_handlers.update_pool(request, pool_id, data)

    router.add_api_operation(
        "/{int:pool_id}",
        ["PATCH"],
        update_pool,
        response={200: PoolOut, 400: ErrorResponse, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER)
    def create_instruction(request, pool_id, instruction: PoolInstructionSchema) -> PoolDetailOut:
        return pool_handlers.create_instruction(request, pool_id, instruction)

    router.add_api_operation(
        "/instruction",
        ["POST"],
        create_instruction,
        response={201: PoolDetailOut, 400: ErrorResponse, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def get_instruction_by_id(request, instruction_id: int) -> PoolInstructionOut:
        return pool_handlers.get_instruction_by_id(request, instruction_id)

    router.add_api_operation(
        "/instruction/{int:instruction_id}",
        ["GET"],
        get_instruction_by_id,
        response={200: PoolInstructionOut, 404: ErrorResponse},
    )

    @has_roles(AuthRole.ADMIN, AuthRole.CUSTOMER, AuthRole.STUDENT)
    def get_instruction_by_pool(request, pool_id: int) -> PoolInstructionOut:
        return pool_handlers.get_instruction_by_pool(request, pool_id)

    router.add_api_operation(
        "/{int:pool_id}/instruction",
        ["GET"],
        get_instruction_by_pool,
        response={200: PoolInstructionOut, 404: ErrorResponse},
    )

    return router


def add_pools_router(api: NinjaAPI, pool_handlers: PoolHandlers):
    pools_router = get_pools_router(pool_handlers)
    api.add_router("/pools", pools_router)
