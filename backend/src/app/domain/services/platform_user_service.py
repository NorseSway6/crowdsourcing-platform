from typing import List
from uuid import UUID

from app.domain.entities.platform_user_schema import UserOut, UserSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.platform_user_interface import IUserRepository
from app.domain.interfaces.skill_interface import ISkillRepository


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        skill_repo: ISkillRepository,
    ):
        self._user_repo = user_repo
        self._skill_repo = skill_repo

    def create_user(self, user_data: UserSchema) -> UserOut:
        return self._user_repo.create_user(user_data)

    def get_all_users(self) -> List[UserOut]:
        return self._user_repo.get_all_users()

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        return self._user_repo.get_user_by_id(user_id)

    def update_user_profile(self, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        return self._user_repo.update_profile(user_id, profile_data)

    def delete_user(self, user_id: UUID) -> bool:
        return self._user_repo.delete_user(user_id)
