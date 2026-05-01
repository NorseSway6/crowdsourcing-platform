from uuid import UUID

from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.task_schema import TaskOut


class IPoolRepository:
    def get_all_pools(self) -> PoolOut:
        pass

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        pass

    def create_pool(self, pool_data: dict) -> PoolOut:
        pass

    def update_pool(self, pool_id: int, pool_data: dict) -> PoolSchema:
        pass

    def create_task(self, pool_id: int, task_data: dict) -> TaskOut:
        pass
