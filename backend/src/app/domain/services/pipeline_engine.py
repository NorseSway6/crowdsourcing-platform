from uuid import UUID

from django.db import transaction

from app.db.models.assignments import Assignment
from app.db.repositories.pipeline_repository import PipelineRepository
from app.domain.entities.pipline_schema import PipelineOut, PipelineSchema
from app.domain.entities.pool_schema import PoolOut
from app.domain.interfaces.assignment_interface import IAssignmentRepository
from app.domain.interfaces.pipeline_interface import IPipelineRepository
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.skill_interface import ISkillRepository
from app.domain.interfaces.task_interface import ITaskRepository
from app.domain.services.consensus_service import ConsensusService


class PipelineEngine(IPipelineRepository):
    def __init__(
        self,
        task_repo: ITaskRepository,
        assignment_repo: IAssignmentRepository,
        consensus_service: ConsensusService,
        pool_repo: IPoolRepository,
        pipeline_repo: IPipelineRepository,
        skill_repo: ISkillRepository,
    ):
        self._task_repo = task_repo
        self._assignment_repo = assignment_repo
        self._consensus_service = consensus_service
        self._pool_repo = pool_repo
        self._pipeline_repo = pipeline_repo
        self._skill_repo = skill_repo

    def create_pools(self, owner_id: UUID, pipeline_data: PipelineSchema) -> PipelineOut:
        with transaction.atomic():
            tasks_qs = self._task_repo.get_unassigned_tasks_by_dataset(pipeline_data.dataset_id)
            if not tasks_qs.exists():
                None

            pipeline = self._pipeline_repo.create_pipeline(owner_id, pipeline_data)

            start_pool = None

            for index, step_data in enumerate(pipeline_data.pools, start=1):
                pool = self._pool_repo.create_pool(pipeline, index, step_data)

                if step_data.skills:
                    skill_names = list(set(step_data.skills))
                    existing_skills = self._skill_repo.get_skills_by_names(skill_names)

                    if len(existing_skills) != len(skill_names):
                        return None

                    pool.skills.add(*existing_skills)

                if index == 1:
                    start_pool = pool

            self._task_repo.link_tasks_to_pool(tasks_qs, start_pool.pool_id, pipeline_data.limit)

        return PipelineOut.from_orm(pipeline)

    def get_pipelines_by_user(self, owner_id: UUID) -> list[PipelineOut]:
        pipelines = self._pipeline_repo.get_pipelines_by_user(owner_id)
        if not pipelines:
            return None
        return [PipelineOut.from_orm(p) for p in pipelines]

    def update_pipeline(self, pipeline_id: int, pipeline_data: PipelineSchema) -> PipelineOut:
        updated = self._pipeline_repo.update_pipeline(pipeline_id, pipeline_data)
        if not updated:
            return None
        return PipelineOut.from_orm(updated)

    def delete_pipeline(self, pipeline_id: int) -> bool:
        deleted = self._pipeline_repo.delete_pipeline(pipeline_id)
        if not deleted:
            return None
        return deleted

    def evaluate_stage_completion(self, task_id: int, current_pool_id: int) -> None:
        consensus_result = self._consensus_service.calculate_pool_consensus(task_id, current_pool_id)

        if not consensus_result.is_consensus_reached:
            return

        all_assignments = self._assignment_repo._get_all_for_task(task_id, current_pool_id)
        for ass in all_assignments:
            is_good = self._consensus_service._are_annotations_similar(
                ass.annotation, consensus_result.final_annotation
            )
            ass.status = Assignment.Status.APPROVED if is_good else Assignment.Status.REJECTED

        self._assignment_repo._bulk_update_assignments(all_assignments)

        is_perfect_consensus = getattr(consensus_result, "confidence", 0) >= 0.95

        next_pool_id = self._get_next_pool_in_pipeline(current_pool_id)

        if next_pool_id and not is_perfect_consensus:
            self._task_repo._move_task_to_pool(
                task_id=task_id,
                new_pool_id=next_pool_id,
                intermediate_data=consensus_result.final_annotation,
            )
        else:
            self._task_repo._mark_task_completed(task_id, consensus_result.final_annotation)

    def _get_next_pool_in_pipeline(self, current_pool_id: int) -> int | None:
        current_pool = self._pool_repo.get_pool_by_id(current_pool_id)
        if not current_pool:
            return None

        next_pool = self._pool_repo.get_next_pool_by_order(
            pipeline_id=current_pool.pipeline_id, current_order=current_pool.order
        )

        return next_pool.pool_id if next_pool else None
