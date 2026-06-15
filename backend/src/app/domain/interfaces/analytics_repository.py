from uuid import UUID

from app.db.models.user_profile import UserProfile
from app.domain.entities.anallytics_schema import PoolsProgressFilter, UserInfoFilter


class IAnalyticsRepository:
    def get_pools_progress(self, user_id: UUID, filters: PoolsProgressFilter) -> list[dict[str, any]]:
        pass

    def get_users_info(self, filters: UserInfoFilter) -> list[UserProfile]:
        pass
