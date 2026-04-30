from app.domain.entities.pool_schema import PoolOut


class IPoolRepository:
    def get_all_pools(self) -> PoolOut:
        pass
