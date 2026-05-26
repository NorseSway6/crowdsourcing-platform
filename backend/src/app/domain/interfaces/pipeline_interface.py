from uuid import UUID

from app.db.models.pipeline import Pipeline
from app.domain.entities.pipeline_schema import PipelineIn


class IPipelineRepository:
    def create_pipeline(self, owner_id: UUID, pipeline_data: PipelineIn) -> Pipeline:
        pass

    def get_pipelines_by_user(self, owner_id: UUID) -> list[Pipeline]:
        pass

    def get_pipeline_by_id(self, pipeline_id: int) -> Pipeline:
        pass

    def update_pipeline(self, pipeline_id: int, pipeline_data: PipelineIn) -> Pipeline:
        pass

    def delete_pipeline(self, pipeline_id: int) -> bool:
        pass
