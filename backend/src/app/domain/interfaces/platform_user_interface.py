from uuid import UUID

from app.db.models.platform_user import PlatformUser
from app.db.models.user_profile import UserProfile
from app.domain.entities.platform_user_schema import UserSchema
from app.domain.entities.user_profile_schema import ProfileSchema


class IUserRepository:
    def create_user(self, user_data: UserSchema) -> PlatformUser:
        pass

    def create_profile(self, user: PlatformUser, profile_data: ProfileSchema) -> UserProfile:
        pass

    def create_new_profile(self, user: PlatformUser) -> UserProfile:
        pass

    def get_all_users(self) -> list[PlatformUser]:
        pass

    def get_user_by_id(self, user_id: UUID) -> PlatformUser:
        pass

    def get_user_profile(self, user_id: UUID) -> UserProfile:
        pass

    def update_profile(self, profile: UserProfile) -> UserProfile:
        pass

    def delete_user(self, user_id: UUID) -> bool:
        pass
