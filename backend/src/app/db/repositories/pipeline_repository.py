from uuid import UUID

from app.db.models.pipeline import Pipeline
from app.domain.entities.pipline_schema import PipelineSchema


class PipelineRepository:
    def create_pipeline(self, owner_id: UUID, pipeline_data: PipelineSchema) -> Pipeline:
        return Pipeline.objects.create(
            owner_id=owner_id,
            dataset_id=pipeline_data.dataset_id,
            name=pipeline_data.name,
            limit=pipeline_data.limit,
        )

    def get_pipelines_by_user(self, owner_id: UUID) -> list[Pipeline]:
        return list(Pipeline.objects.filter(owner_id=owner_id).all())

    def update_pipeline(self, pipeline_id: int, pipeline_data: PipelineSchema) -> Pipeline:
        pipeline = Pipeline.objects.filter(pipeline_id=pipeline_id).first()
        if not pipeline:
            return None

        pipeline.name = pipeline_data.name
        pipeline.save()
        return pipeline

    def delete_pipeline(self, pipeline_id: int) -> bool:
        pipeline = Pipeline.objects.filter(pipeline_id=pipeline_id).first()
        if not pipeline:
            return False

        pipeline.delete()
        return True
