from app.db.models.pool import Pool
from app.domain.entities.pool_schema import PoolOut
from app.domain.interfaces.pool_repository_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self) -> PoolOut:
        return Pool.objects.all()
