from app.db.models.pipeline import Pipeline
from app.domain.entities.pipline_schema import PipelineSchema


class IPipelineRepository:
    def create_pipeline(self, pipeline_data: PipelineSchema) -> Pipeline:
        pass
