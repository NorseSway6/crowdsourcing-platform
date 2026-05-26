from typing import List

from django.db import transaction

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
        pools = self._pool_repo.get_all_pools()
        if not pools:
            return None
        return [PoolOut.from_orm(pool) for pool in pools]

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        pool = self._pool_repo.get_pool_by_id(pool_id)
        if not pool:
            return None
        return PoolOut.from_orm(pool)

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        with transaction.atomic():
            pool = self._pool_repo.get_pool_by_id(pool_id)
            if not pool:
                return None

            if pool_data.skills:
                skill_names = list(set(pool_data.skills))
                existing_skills = self._skill_repo.get_skills_by_names(skill_names)

                if existing_skills.count() != len(skill_names):
                    return None

                pool.skills.set(existing_skills)

            for attr, value in pool_data.items():
                if attr != "skills":
                    setattr(pool, attr, value)

            updated = self._pool_repo.update_pool(pool)
            if not updated:
                return None

            return PoolOut.from_orm(pool)
