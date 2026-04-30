from typing import List
from uuid import UUID

from app.domain.entities.platform_user_schema import UserIn, UserOut


class IUserRepository:
    def get_or_create_user(self, user_id: UUID, params: dict) -> UserOut:
        pass

    def get_all_users(self) -> List[UserOut]:
        pass

    def get_user_by_id(self, user_id: UUID) -> UserOut:
        pass
