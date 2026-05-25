from typing import List
from uuid import UUID

from app.db.models.pool import Pool
from app.domain.entities.pool_schema import PoolOut, PoolSchema


class IPoolRepository:
    def get_all_pools(self) -> List[PoolOut]:
        pass

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        pass

    def create_pool(self, pipeline_id, index, pool_data: PoolSchema) -> Pool:
        pass

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        pass
