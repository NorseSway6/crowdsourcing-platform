from typing import List
from uuid import UUID

from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.entities.skill_schema import SkillSchema
from app.domain.entities.user_profile_schema import ProfileSchema


class IProfileRepository:
    def set_profile(self, user: UserIn, profile_data: dict) -> ProfileSchema:
        pass

    def update_user_profile(self, user_id: UUID, profile_data: ProfileSchema) -> ProfileSchema:
        pass
