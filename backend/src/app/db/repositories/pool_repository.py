from uuid import UUID

from app.db.models.pool import Pool
from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self) -> PoolOut:
        return Pool.objects.all()

    def create_pool(self, pool_data: dict) -> PoolOut:
        pool = Pool.objects.create(**pool_data)
        return pool

    def update_pool(self, pool_id: int, pool_data: dict) -> PoolSchema:
        Pool.objects.filter(pool_id=pool_id).update(**pool_data)
        return Pool.objects.get(pool_id=pool_id)
