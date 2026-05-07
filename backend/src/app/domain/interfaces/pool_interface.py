from typing import List
from uuid import UUID

from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.task_schema import TaskOut, TaskSchema


class IPoolRepository:
    def get_all_pools(self) -> List[PoolOut]:
        pass

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        pass

    def create_pool(self, pool_data: PoolSchema) -> PoolOut:
        pass

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        pass

    def create_task(self, pool_id: int, task_data: TaskSchema) -> TaskOut:
        pass

    def delete_pool(self, pool_id: int) -> bool:
        pass
