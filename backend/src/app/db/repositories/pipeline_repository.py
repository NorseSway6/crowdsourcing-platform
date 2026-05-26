from uuid import UUID

from django.db import IntegrityError

from app.db.models.pipeline import Pipeline
from app.domain.entities.pipline_schema import PipelineSchema


class PipelineRepository:
    def create_pipeline(self, owner_id: UUID, pipeline_data: PipelineSchema) -> Pipeline:
        try:
            pipeline = Pipeline.objects.create(
                owner_id=owner_id,
                dataset_id=pipeline_data.dataset_id,
                name=pipeline_data.name,
                limit=pipeline_data.limit,
            )
        except IntegrityError:
            return None

        return pipeline

    def get_pipelines_by_user(self, owner_id: UUID) -> list[Pipeline]:
        return list(Pipeline.objects.filter(owner_id=owner_id).all())

    def get_pipeline_by_id(self, pipeline_id: int) -> Pipeline:
        return Pipeline.objects.filter(pipeline_id=pipeline_id).first()

    def update_pipeline(self, pipeline_id: int, pipeline_data: PipelineSchema) -> Pipeline:
        updated = Pipeline.objects.filter(pipeline_id=pipeline_id).update(name=pipeline_data.name)
        return updated > 0

    def delete_pipeline(self, pipeline_id: int) -> bool:
        deleted, _ = Pipeline.objects.filter(pipeline_id=pipeline_id).delete()
        return deleted > 0
