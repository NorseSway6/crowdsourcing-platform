from app.db.models.pool import Pool
from app.domain.entities.pool_schema import PoolSchema


class IPoolRepository:
    def get_all_pools(self) -> list[Pool]:
        pass

    def get_pool_by_id(self, pool_id: int) -> Pool:
        pass

    def get_next_pool_by_order(self, pipeline_id: int, current_order: int) -> Pool:
        pass

    def create_pool(self, pipeline, index, pool_data: PoolSchema) -> Pool:
        pass

    def update_pool(self, pool: Pool) -> Pool:
        pass
