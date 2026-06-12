from uuid import UUID

from django.db.models import Count, Q

from app.db.models.pool import Pool
from app.db.models.user_profile import UserProfile
from app.domain.entities.anallytics_schema import PoolsProgressFilter, UserInfoFilter


class AnalyticsRepository:

    def get_pools_progress(self, user_id: UUID, filters: PoolsProgressFilter) -> list[dict[str, any]]:
        queryset = Pool.objects.filter(pipeline__owner__user_id=user_id)

        if filters.pipline_id:
            queryset = queryset.filter(pipeline_id=filters.pipline_id)

        if filters.pool_type:
            queryset = queryset.filter(pool_type=filters.pool_type)

        pools = list(
            queryset.annotate(
                total_tasks_count=Count("assignment_pool__task_id", distinct=True),
                completed_tasks_count=Count(
                    "assignment_pool__task_id", filter=Q(assignment_pool__status="APPROVED"), distinct=True
                ),
            ).values("pool_id", "pool_type", "total_tasks_count", "completed_tasks_count")
        )

        return pools

    def get_users_info(self, filters: UserInfoFilter) -> list[UserProfile]:
        queryset = UserProfile.objects.prefetch_related("skills").all()

        if filters.first_name:
            queryset = queryset.filter(first_name=filters.first_name)

        if filters.last_name:
            queryset = queryset.filter(last_name=filters.last_name)

        if filters.group:
            queryset = queryset.filter(group=filters.group)

        if filters.institution:
            queryset = queryset.filter(institution=filters.institution)

        users = list(
            queryset.annotate(
                total_submitted=Count(
                    "user__assignment_user",
                    filter=Q(user__assignment_user__status__in=["APPROVED", "REJECTED"]),
                    distinct=True,
                ),
                total_approved=Count(
                    "user__assignment_user", filter=Q(user__assignment_user__status="APPROVED"), distinct=True
                ),
            )
        )

        return users
