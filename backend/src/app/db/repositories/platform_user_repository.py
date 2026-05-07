from typing import List
from uuid import UUID

from django.db import transaction
from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.platform_user import PlatformUser
from app.db.models.skill import Skill
from app.db.models.user_profile import UserProfile
from app.domain.entities.platform_user_schema import UserOut, UserSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.platform_user_interface import IUserRepository


class UserRepository(IUserRepository):
    def create_user(self, user_data: UserSchema) -> UserOut:
        try:
            with transaction.atomic():
                user = PlatformUser.objects.create(email=user_data.email, role=user_data.role)

                if user_data.profile:
                    profile_data = user_data.profile

                    profile_obj = UserProfile.objects.create(
                        user=user,
                        last_name=profile_data.last_name,
                        first_name=profile_data.first_name,
                        middle_name=profile_data.middle_name,
                        group=profile_data.group,
                        institution=profile_data.institution,
                    )

                    if profile_data.skills:
                        skill_names = list({s.name for s in profile_data.skills})

                        existing_skills = Skill.objects.filter(name__in=skill_names)

                        if len(existing_skills) != len(skill_names):
                            raise HttpError(404, "Some skills not found")
                        profile_obj.skills.add(*existing_skills)
        except IntegrityError:
            raise HttpError(409, "User with this email already exists")

        return UserOut.from_orm(user)

    def get_all_users(self) -> List[UserOut]:
        users = PlatformUser.objects.select_related("user_profile").all()
        if not users:
            raise HttpError(404, "Users not found")
        return [UserOut.from_orm(u) for u in users]

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        user = PlatformUser.objects.select_related("user_profile").filter(user_id=user_id).first()
        if user is None:
            raise HttpError(404, "User not found")
        return UserOut.from_orm(user)

    def update_profile(self, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        try:
            with transaction.atomic():
                user = PlatformUser.objects.select_related("user_profile").filter(user_id=user_id).first()
                if not user:
                    raise HttpError(404, "User not found")

                profile = getattr(user, "user_profile", None)

                if not profile:
                    profile = UserProfile(user=user)

                if profile_data.skills:
                    skill_names = list({s.name for s in profile_data.skills})
                    existing_skills = Skill.objects.filter(name__in=skill_names)

                    if len(existing_skills) != len(skill_names):
                        raise HttpError(404, "Some skills not found")

                    profile.skills.set(existing_skills)

                update_fields = profile_data.dict(exclude={"skills"}, exclude_unset=True)
                for attr, value in update_fields.items():
                    setattr(profile, attr, value)

                profile.save()

        except IntegrityError:
            raise HttpError(409, "Update failed due to integrity error")

        return UserOut.from_orm(user)

    def delete_user(self, user_id: UUID) -> bool:
        deleted, _ = PlatformUser.objects.filter(user_id=user_id).delete()
        if not deleted:
            raise HttpError(404, "User for delete not found")
        return deleted
