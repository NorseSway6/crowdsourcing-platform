from typing import List

from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.skill_interface import ISkillRepository
from app.domain.interfaces.task_interface import ITaskRepository


class PoolService:
    def __init__(self, pool_repo: IPoolRepository, skill_repo: ISkillRepository, task_repo: ITaskRepository):
        self._pool_repo = pool_repo
        self._skill_repo = skill_repo
        self._task_repo = task_repo

    def get_all_pools(self) -> List[PoolOut]:
        return self._pool_repo.get_all_pools()

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        return self._pool_repo.get_pool_by_id(pool_id)

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        return self._pool_repo.update_pool(pool_id, pool_data)
