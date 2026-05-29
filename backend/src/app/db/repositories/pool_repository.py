from django.db import IntegrityError

from app.db.models.pool import Pool
from app.domain.entities.pool_schema import PoolFilter, PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self, filters: PoolFilter) -> list[Pool]:
        queryset = Pool.objects.prefetch_related("skills")

        if filters.skills:
            queryset = queryset.filter(skills__name__in=filters.skills).distinct()

        if filters.max_points:
            queryset = queryset.filter(points__lte=filters.max_points)

        if filters.min_points:
            queryset = queryset.filter(points__gte=filters.min_points)

        if filters.institution:
            queryset = queryset.filter(target_institution=filters.institution)

        # добавить расчет выполения пулла (pool status = COMPLETED)

        return list(queryset.all())

    def get_pool_by_id(self, pool_id: int) -> Pool:
        return Pool.objects.filter(pool_id=pool_id).first()

    def get_next_pool_by_order(self, pipeline_id: int, current_order: int) -> Pool:
        return Pool.objects.filter(pipeline_id=pipeline_id, order=current_order + 1).first()

    def create_pool(self, pipeline, index, pool_data: PoolSchema) -> Pool:
        try:
            pool = Pool.objects.create(
                pipeline=pipeline,
                order=index,
                points=pool_data.points,
                overlap=pool_data.overlap,
                pool_type=pool_data.pool_type,
                target_institution=pool_data.institution,
            )
        except IntegrityError:
            return None

        return pool

    def update_pool(self, pool: Pool) -> Pool:
        try:
            pool.save()
        except IntegrityError:
            return None

        return pool
