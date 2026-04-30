from typing import List
from uuid import UUID

from app.db.models.platform_user import PlatformUser
from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.interfaces.platform_user_interface import IUserRepository


class UserRepository(IUserRepository):
    def get_or_create_user(self, user_id: UUID, params: dict) -> UserOut:
        user, _ = PlatformUser.objects.get_or_create(user_id=user_id, defaults=params)
        return user

    def get_all_users(self) -> List[UserOut]:
        return PlatformUser.objects.select_related("user_profile").all()

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        return PlatformUser.objects.select_related("user_profile").filter(user_id=user_id).first()
