from django.db import IntegrityError

from app.db.models.pool import Pool
from app.domain.entities.pool_schema import PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self) -> list[Pool]:
        return list(Pool.objects.all())

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
