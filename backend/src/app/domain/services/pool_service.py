from app.domain.interfaces.pool_interface import IPoolRepository


class PoolService:
    def __init__(self, pool_repo: IPoolRepository):
        self._pool_repo = pool_repo

    def get_all_pools(self):
        return self._pool_repo.get_all_pools()
