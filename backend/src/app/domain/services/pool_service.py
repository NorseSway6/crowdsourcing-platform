from typing import List

from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.skill_interface import ISkillRepository


class PoolService:
    def __init__(self, pool_repo: IPoolRepository, skill_repo: ISkillRepository):
        self._pool_repo = pool_repo
        self._skill_repo = skill_repo

    def get_all_pools(self) -> List[PoolOut]:
        return self._pool_repo.get_all_pools()

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        return self._pool_repo.get_pool_by_id(pool_id)

    def create_pool(self, pool_data: PoolSchema) -> PoolOut:
        return self._pool_repo.create_pool(pool_data)

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        return self._pool_repo.update_pool(pool_id, pool_data)

    def create_task(self, pool_id: int, task_data: TaskSchema) -> TaskOut:
        data = task_data.dict()
        dataset_id = data.pop("dataset_id")
        return self._pool_repo.create_task(pool_id, dataset_id, data)

    def delete_pool(self, pool_id: int) -> bool:
        return self._pool_repo.delete_pool(pool_id)
