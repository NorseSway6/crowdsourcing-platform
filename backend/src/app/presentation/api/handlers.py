from typing import List
from uuid import UUID

from ninja import Body, Path

from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.entities.pool_schema import PoolOut
from app.domain.entities.skill_schema import SkillSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.services.platform_user_service import UserService
from app.domain.services.pool_service import PoolService
from app.domain.services.skill_service import SkillService


class SkillHandlers:
    def __init__(self, skill_service: SkillService):
        self._skill_service = skill_service

    def get_all_skills(self, request) -> List[SkillSchema]:
        return self._skill_service.get_all_skills()


class PoolHandlers:
    def __init__(self, pool_service: PoolService):
        self._pool_service = pool_service

    def get_all_pools(self, request) -> List[PoolOut]:
        return self._pool_service.get_all_pools()


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def get_or_create_user(self, request, user_data: UserIn = Body(...)) -> UserOut:
        return self._user_service.get_or_create_user(user_data)

    def get_all_users(self, request) -> UserOut:
        return self._user_service.get_all_users()

    def get_user_by_id(self, request, user_id: UUID = Path(...)):
        return self._user_service.get_user_by_id(user_id)

    def update_user_profile(self, request, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        return self._user_service.update_user_profile(user_id, profile_data)
