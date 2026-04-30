from uuid import UUID

from app.domain.entities.pool_schema import PoolOut, PoolSchema


class IPoolRepository:
    def get_all_pools(self) -> PoolOut:
        pass

    def create_pool(self, pool_data: PoolSchema) -> PoolOut:
        pass

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolSchema:
        pass
