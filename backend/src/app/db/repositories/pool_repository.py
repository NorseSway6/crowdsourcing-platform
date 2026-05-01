from uuid import UUID

from app.db.models.pool import Pool
from app.db.models.task import Task
from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.task_schema import TaskOut
from app.domain.interfaces.pool_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self) -> PoolOut:
        return Pool.objects.all()

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        return Pool.objects.filter(pool_id=pool_id).first()

    def create_pool(self, pool_data: dict) -> PoolOut:
        pool = Pool.objects.create(**pool_data)
        return pool

    def update_pool(self, pool_id: int, pool_data: dict) -> PoolSchema:
        Pool.objects.filter(pool_id=pool_id).update(**pool_data)
        return Pool.objects.get(pool_id=pool_id)

    def create_task(self, pool_id: int, dataset_id: int, task_data: dict) -> TaskOut:
        task = Task.objects.create(pool_id=pool_id, dataset_id=dataset_id, **task_data)
        return task
