from uuid import UUID

from app.domain.entities.anallytics_schema import PoolProgressOut, PoolsProgressFilter, UserInfoFilter, UserInfoOut
from app.domain.interfaces.analytics_repository import IAnalyticsRepository


class AnalyticsService:
    def __init__(self, analytics_repo: IAnalyticsRepository):
        self._analytics_repo = analytics_repo

    def get_pools_progress(self, user_id: UUID, filters: PoolsProgressFilter) -> list[PoolProgressOut]:
        raw_data = self._analytics_repo.get_pools_progress(user_id, filters)

        progress_list = []
        for item in raw_data:
            total = item["total_tasks_count"]
            completed = item["completed_tasks_count"]

            percentage = round((completed / total) * 100, 2) if total > 0 else 0.0

            progress_list.append(
                PoolProgressOut(
                    pool_id=item["pool_id"],
                    pool_type=item["pool_type"],
                    total_tasks=total,
                    completed_tasks=completed,
                    progress_percentage=percentage,
                )
            )

        return [PoolProgressOut.from_orm(p) for p in progress_list]

    def get_users_info(self, filters: UserInfoFilter) -> list[UserInfoOut]:
        raw_data = self._analytics_repo.get_users_info(filters)

        users_info = []
        for item in raw_data:
            submitted = item.total_submitted
            approved = item.total_approved

            accuracy = (approved / submitted * 100) if submitted > 0 else 100.0

            users_info.append(
                UserInfoOut(
                    last_name=item.last_name,
                    first_name=item.first_name,
                    middle_name=item.middle_name,
                    group=item.group,
                    institution=item.institution,
                    submitted=submitted,
                    approved=approved,
                    user_accuracy=accuracy,
                )
            )
        return [UserInfoOut.from_orm(u) for u in users_info]
