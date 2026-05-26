from typing import List
from uuid import UUID

from django.db import transaction

from app.domain.entities.platform_user_schema import UserOut, UserSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.platform_user_interface import IUserRepository
from app.domain.interfaces.skill_interface import ISkillRepository


class UserService:
    def __init__(self, user_repo: IUserRepository, skill_repo: ISkillRepository):
        self._user_repo = user_repo
        self._skill_repo = skill_repo

    def create_user(self, user_data: UserSchema) -> UserOut:
        with transaction.atomic():
            user = self._user_repo.create_user(user_data)
            if not user:
                return None

            if user_data.profile:
                profile_data = user_data.profile

                profile = self._user_repo.create_profile(user, profile_data)
                if not profile:
                    return None

                if profile_data.skills:
                    skill_names = list(set(profile_data.skills))
                    existing_skills = self._skill_repo.get_skills_by_names(skill_names)
                    if not existing_skills:
                        return None

                    if len(existing_skills) != len(skill_names):
                        return None

                    profile.skills.add(*existing_skills)

            return UserOut.from_orm(user)

    def get_all_users(self) -> List[UserOut]:
        users = self._user_repo.get_all_users()
        if not users:
            return None
        return [UserOut.from_orm(u) for u in users]

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        user = self._user_repo.get_user_by_id(user_id)
        if not user:
            return None
        return UserOut.from_orm(user)

    def update_user_profile(self, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        with transaction.atomic():
            user = self._user_repo.get_user_profile(user_id)
            if not user:
                return None

            profile = getattr(user, "user_profile", None)
            if not profile:
                profile = self._user_repo.create_new_profile(user)
                if not profile:
                    return None

            if profile_data.skills:
                skill_names = list(set(profile_data.skills))
                existing_skills = self._skill_repo.get_skills_by_names(skill_names)
                if not existing_skills:
                    return None

                if len(existing_skills) != len(skill_names):
                    return None

            for attr, value in profile_data.items():
                if attr != "skills":
                    setattr(profile, attr, value)

            updated = self._user_repo.update_profile(profile)
            if not updated:
                return None

            return UserOut.from_orm(updated)

    def delete_user(self, user_id: UUID) -> bool:
        deleted = self._user_repo.delete_user(user_id)
        if not deleted:
            return None
        return deleted
