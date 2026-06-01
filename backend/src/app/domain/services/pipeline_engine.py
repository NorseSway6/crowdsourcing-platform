from uuid import UUID

from django.db import transaction

from app.db.models.pool import Pool
from app.domain.entities.consensus_schema import ConsensusSchema
from app.domain.entities.pipeline_schema import PipelineIn, PipelineOut
from app.domain.interfaces.assignment_interface import IAssignmentRepository
from app.domain.interfaces.pipeline_interface import IPipelineRepository
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.skill_interface import ISkillRepository
from app.domain.interfaces.task_interface import ITaskRepository
from app.domain.services.consensus_service import ConsensusService
from app.domain.services.pool_service import PoolService
from app.domain.services.task_service import TaskService


class PipelineEngine(IPipelineRepository):
    def __init__(
        self,
        task_repo: ITaskRepository,
        assignment_repo: IAssignmentRepository,
        consensus_service: ConsensusService,
        pool_repo: IPoolRepository,
        pipeline_repo: IPipelineRepository,
        skill_repo: ISkillRepository,
        task_service: TaskService,
        pool_service: PoolService,
    ):
        self._task_repo = task_repo
        self._assignment_repo = assignment_repo
        self._consensus_service = consensus_service
        self._pool_repo = pool_repo
        self._pipeline_repo = pipeline_repo
        self._skill_repo = skill_repo
        self._task_service = task_service
        self._pool_service = pool_service

    def create_pools(self, owner_id: UUID, pipeline_data: PipelineIn) -> PipelineOut:
        with transaction.atomic():
            tasks = self._task_repo.get_unassigned_tasks_by_dataset(pipeline_data.dataset_id)
            if not tasks:
                return None

            pipeline = self._pipeline_repo.create_pipeline(owner_id, pipeline_data)
            if not pipeline:
                return None

            start_pool = None
            for index, step_data in enumerate(pipeline_data.pools, start=1):
                pool = self._pool_service.create_pool(pipeline, index, step_data)
                if not pool:
                    return None

                if index == 1:
                    start_pool = pool

            linked = self._task_service.link_tasks_to_pool(tasks, start_pool.pool_id, pipeline_data.limit)
            if not linked:
                return None

            return PipelineOut.from_orm(pipeline)

    def get_pipelines_by_user(self, owner_id: UUID) -> list[PipelineOut]:
        pipelines = self._pipeline_repo.get_pipelines_by_user(owner_id)
        if not pipelines:
            return None
        return [PipelineOut.from_orm(p) for p in pipelines]

    def update_pipeline(self, pipeline_id: int, pipeline_data: PipelineIn) -> PipelineOut:
        updated = self._pipeline_repo.update_pipeline(pipeline_id, pipeline_data)
        if not updated:
            return None

        pipeline = self._pipeline_repo.get_pipeline_by_id(pipeline_id)
        return PipelineOut.from_orm(pipeline)

    def delete_pipeline(self, pipeline_id: int) -> bool:
        deleted = self._pipeline_repo.delete_pipeline(pipeline_id)
        if not deleted:
            return None
        return deleted

    def evaluate_stage_completion(self, task_id: int, current_pool_id: int) -> None:
        consensus_result = self._consensus_service.calculate_pool_consensus(task_id, current_pool_id)
        if not consensus_result.is_consensus_reached:
            return

        with transaction.atomic():
            assignments = self._consensus_service._resolve_assignments(task_id, current_pool_id, consensus_result)
            if not assignments:
                return
            self._assignment_repo._bulk_update_assignments(assignments)

            current_pool = self._pool_repo.get_pool_by_id(current_pool_id)
            if not current_pool:
                return

            if current_pool.pool_type == Pool.PoolType.ANNOTATION:
                self._resolve_annotation(task_id, current_pool_id, consensus_result)
            elif current_pool.pool_type == Pool.PoolType.VERIFICATION:
                annotation_pool = self._pool_repo._get_pool_by_type(
                    pipeline_id=current_pool.pipeline_id, pool_type=Pool.PoolType.ANNOTATION
                )
                if not annotation_pool:
                    return
                self._resolve_verification(task_id, current_pool_id, annotation_pool, consensus_result)

    def _resolve_annotation(self, task_id: int, current_pool_id: int, consensus_result: ConsensusSchema) -> None:
        next_pool_id = self._pool_service._get_next_pool_in_pipeline(current_pool_id)
        if not next_pool_id:
            marked = self._task_repo._mark_task_completed(task_id, current_pool_id)
            if not marked:
                return
            return

        moved = self._task_repo._move_task_to_pool(
            task_id=task_id,
            new_pool_id=next_pool_id,
            intermediate_data=consensus_result.final_annotation,
        )
        if not moved:
            return

    def _resolve_verification(
        self, task_id: int, current_pool_id: int, annotation_pool: Pool, consensus_result: ConsensusSchema
    ) -> None:
        if consensus_result.verdict == "APPROVED":
            approved = self._assignment_repo._approve_assignment_for_task(task_id, annotation_pool.pool_id)
            if not approved:
                return
            next_pool_id = self._pool_service._get_next_pool_in_pipeline(current_pool_id)
            if not next_pool_id:
                marked = self._task_repo._mark_task_completed(task_id, current_pool_id)
                if not marked:
                    return
                self._pool_service.try_complete_pool(current_pool_id)
                self._pool_service.try_complete_pool(annotation_pool.pool_id)
                return

            moved = self._task_repo._move_task_to_pool(
                task_id=task_id,
                new_pool_id=next_pool_id,
                intermediate_data=consensus_result.final_annotation,
            )
            if not moved:
                return

        elif consensus_result.verdict == "REJECTED":
            self._task_service._move_task_to_annotation_retry(task_id, current_pool_id)

            rejected = self._assignment_repo._reject_assignment_for_task(task_id, annotation_pool.pool_id)
            if not rejected:
                return

            if annotation_pool and annotation_pool.status == Pool.PoolStatus.COMPLETED:
                marked1 = self._pool_repo._mark_pool_open(annotation_pool.pool_id)
                if not marked1:
                    return
                marked2 = self._pool_repo._mark_pool_open(current_pool_id)
                if not marked2:
                    return

            archided = self._assignment_repo.archive_assignments_for_task(task_id, current_pool_id)
            if not archided:
                return
            return
