from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.skill_interface import ISkillRepository


class PoolService:
    def __init__(self, pool_repo: IPoolRepository, skill_repo: ISkillRepository):
        self._pool_repo = pool_repo
        self._skill_repo = skill_repo

    def get_all_pools(self):
        return self._pool_repo.get_all_pools()

    def create_pool(self, pool_data: PoolSchema) -> PoolOut:
        data = pool_data.dict()
        skills_data = data.pop("skills", None)

        pool = self._pool_repo.create_pool(data)

        if skills_data is not None:
            self._skill_repo.set_skills(pool, skills_data)

        return pool

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolSchema:
        update_data = pool_data.dict(exclude_unset=True)
        skills_data = update_data.pop("skills", None)

        pool = self._pool_repo.update_pool(pool_id, update_data)

        if skills_data is not None:
            self._skill_repo.set_skills(pool, skills_data)

        return pool
