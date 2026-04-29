from typing import List

from app.domain.entities.pool_schema import PoolOut
from app.domain.entities.skill_schema import SkillSchema
from app.domain.services.skill_service import SkillService


class SkillHandlers:
    def __init__(self, skill_service: SkillService):
        self._skill_service = skill_service

    def get_all_skills(self, request) -> List[SkillSchema]:
        return self._skill_service.get_all_skills()


class PoolHandlers:
    def __init__(self, pool_service):
        self._pool_service = pool_service

    def get_all_pools(self, request) -> List[PoolOut]:
        return self._pool_service.get_all_pools()
