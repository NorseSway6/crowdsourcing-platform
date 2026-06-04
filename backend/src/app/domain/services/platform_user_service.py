from uuid import UUID

from django.db import transaction

import app.domain.exceptions as exc
from app.domain.entities.platform_user_schema import RegisterSchema, UserOut
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.platform_user_interface import IUserRepository
from app.domain.interfaces.skill_interface import ISkillRepository


class UserService:
    def __init__(self, user_repo: IUserRepository, skill_repo: ISkillRepository):
        self._user_repo = user_repo
        self._skill_repo = skill_repo

    def create_user(self, user_data: RegisterSchema) -> UserOut:
        is_unique_email = self._user_repo.is_unique_email(user_data.email)
        if not is_unique_email:
            return None

        with transaction.atomic():
            user = self._user_repo.create_user(user_data)
            if not user:
                raise exc.UserCreationFailedError()

            if user_data.user_profile:
                profile_data = user_data.user_profile

                profile = self._user_repo.create_profile(user, profile_data)
                if not profile:
                    raise exc.ProfileCreationFailedError()

                if profile_data.skills:
                    skill_names = list(set(profile_data.skills))
                    existing_skills = self._skill_repo.get_skills_by_names(skill_names)
                    if not existing_skills:
                        raise exc.SkillNotFoundError()

                    if len(existing_skills) != len(skill_names):
                        raise exc.SkillNotFoundError()

                    profile.skills.add(*existing_skills)

            return UserOut.from_orm(user)

    def get_all_users(self) -> list[UserOut]:
        users = self._user_repo.get_all_users()
        if not users:
            raise exc.UserNotFoundError()
        return [UserOut.from_orm(u) for u in users]

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        user = self._user_repo.get_user_by_id(user_id)
        if not user:
            raise exc.UserNotFoundError()
        return UserOut.from_orm(user)

    def update_user_profile(self, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        with transaction.atomic():
            user = self._user_repo.get_user_profile(user_id)
            if not user:
                raise exc.UserNotFoundError()

            profile = getattr(user, "user_profile", None)
            if not profile:
                profile = self._user_repo.create_new_profile(user)
                if not profile:
                    raise exc.ProfileCreationFailedError()

            if profile_data.skills:
                skill_names = list(set(profile_data.skills))
                existing_skills = self._skill_repo.get_skills_by_names(skill_names)
                if not existing_skills:
                    raise exc.SkillNotFoundError()

                if len(existing_skills) != len(skill_names):
                    raise exc.SkillNotFoundError()

                profile.skills.set(existing_skills)

            update_fields = profile_data.dict(exclude={"skills"}, exclude_unset=True)
            for attr, value in update_fields.items():
                setattr(profile, attr, value)

            updated = self._user_repo.update_profile(profile)
            if not updated:
                raise exc.ProifleUpdatingError()

            return UserOut.from_orm(user)

    def delete_user(self, user_id: UUID) -> bool:
        deleted = self._user_repo.delete_user(user_id)
        if not deleted:
            raise exc.UserDeletionError()
        return deleted
