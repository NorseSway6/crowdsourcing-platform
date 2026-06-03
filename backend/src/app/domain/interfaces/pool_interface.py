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

    def _mark_pool_completed(self, pool_id: int) -> bool:
        pass

    def _mark_pool_open(self, pool_id: int) -> bool:
        pass

    def _get_pool_by_type(self, pipeline_id: int, pool_type: str) -> Pool | None:
        pass
