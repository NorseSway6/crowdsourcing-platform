from typing import List
from uuid import UUID

from app.domain.entities.platform_user_schema import UserOut, UserSchema
from app.domain.entities.user_profile_schema import ProfileSchema


class IUserRepository:
    def create_user(self, user_data: UserSchema) -> UserOut:
        pass

    def get_all_users(self) -> List[UserOut]:
        pass

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        pass

    def update_profile(self, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        pass

    def delete_user(self, user_id: UUID) -> bool:
        pass
