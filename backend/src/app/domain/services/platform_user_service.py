from uuid import UUID

from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.platform_user_interface import IUserRepository
from app.domain.interfaces.user_profile_interface import IProfileRepository


class UserService:
    def __init__(self, user_repo: IUserRepository, profile_repo: IProfileRepository):
        self._user_repo = user_repo
        self._profile_repo = profile_repo

    def get_or_create_user(self, user_data: UserIn) -> UserOut:
        data = user_data.dict(exclude_unset=True)
        profile_data = data.pop("profile", None)
        user_id = data.pop("user_id")

        user = self._user_repo.get_or_create_user(user_id, data)

        if profile_data:
            skills_list = profile_data.pop("skills", [])
            profile = self._profile_repo.set_profile(user, profile_data)

            self._profile_repo.set_skills(profile, skills_list)

            user.profile = profile

        return user

    def get_all_users(self) -> UserOut:
        return self._user_repo.get_all_users()

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        return self._user_repo.get_user_by_id(user_id)

    def update_user_profile(self, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        update_data = profile_data.dict(exclude_unset=True)
        skills_data = update_data.pop("skills", None)

        profile = self._profile_repo.update_profile(user_id, update_data)

        self._profile_repo.set_skills(profile, skills_data)

        return self._user_repo.get_or_create_user(user_id, update_data)
