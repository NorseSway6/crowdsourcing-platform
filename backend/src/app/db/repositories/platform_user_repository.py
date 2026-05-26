from uuid import UUID

from django.db import IntegrityError

from app.db.models.platform_user import PlatformUser
from app.db.models.user_profile import UserProfile
from app.domain.entities.platform_user_schema import UserSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.platform_user_interface import IUserRepository


class UserRepository(IUserRepository):
    def create_user(self, user_data: UserSchema) -> PlatformUser:
        try:
            user = PlatformUser.objects.create(email=user_data.email, role=user_data.role)
        except IntegrityError:
            return None

        return user

    def create_profile(self, user: PlatformUser, profile_data: ProfileSchema) -> UserProfile:
        try:
            profile = UserProfile.objects.create(
                user=user,
                last_name=profile_data.last_name,
                first_name=profile_data.first_name,
                middle_name=profile_data.middle_name,
                group=profile_data.group,
                institution=profile_data.institution,
            )
        except IntegrityError:
            return None

        return profile

    def create_new_profile(self, user: PlatformUser) -> UserProfile:
        return UserProfile.objects.create(user=user)

    def get_all_users(self) -> list[PlatformUser]:
        return list(PlatformUser.objects.select_related("user_profile").all())

    def get_user_by_id(self, user_id: UUID) -> PlatformUser:
        return PlatformUser.objects.select_related("user_profile").filter(user_id=user_id).first()

    def get_user_profile(self, user_id: UUID) -> UserProfile:
        return PlatformUser.objects.select_related("user_profile").filter(user_id=user_id).first()

    def update_profile(self, profile: UserProfile) -> UserProfile:
        try:
            profile.save()
        except IntegrityError:
            return None

        return profile

    def delete_user(self, user_id: UUID) -> bool:
        deleted, _ = PlatformUser.objects.filter(user_id=user_id).delete()
        return deleted > 0
