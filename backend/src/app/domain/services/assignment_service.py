from datetime import timedelta
from uuid import UUID

from django.db import transaction
from django.utils import timezone

import app.domain.exceptions as exc
from app.db.models.assignments import Assignment
from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.interfaces.assignment_interface import IAssignmentRepository
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.task_interface import ITaskRepository
from app.domain.services.pipeline_engine import PipelineEngine


class AssignmentService:
    def __init__(
        self,
        assignment_repo: IAssignmentRepository,
        task_repo: ITaskRepository,
        pipeline_engine: PipelineEngine,
        pool_repo: IPoolRepository,
    ):
        self._assignment_repo = assignment_repo
        self._task_repo = task_repo
        self._pipeline_engine = pipeline_engine
        self._pool_repo = pool_repo

    def get_assignments_by_user(self, user_id: UUID) -> list[AssignmentOut]:
        assignments = self._assignment_repo.get_assignments_by_user(user_id)
        if not assignments:
            raise exc.AssignmentNotFoundError()
        return [AssignmentOut.from_orm(a) for a in assignments]

    def get_completed_assignments_by_user(self, user_id: UUID) -> list[AssignmentOut]:
        assignments = self._assignment_repo.get_completed_assignments_by_user(user_id)
        if not assignments:
            raise exc.AssignmentNotFoundError()
        return [AssignmentOut.from_orm(a) for a in assignments]

    def create_assignment(self, user_id: UUID, pool_id: int) -> AssignmentOut:
        assignmented_task = self._assignment_repo._get_active_assignment(user_id)
        if assignmented_task:
            return AssignmentOut.from_orm(assignmented_task)
        if not assignmented_task:
            raise exc.AssignmentNotFoundError()

        with transaction.atomic():
            task = self._task_repo.get_next_task(user_id, pool_id)
            if not task:
                raise exc.TaskNotFoundError()

            pool = self._pool_repo.get_pool_by_id(pool_id)
            if not pool:
                raise exc.PoolNotFoundError()
            expires_at = timezone.now() + timedelta(seconds=pool.time_limit)

            assignment = self._assignment_repo.create_assignment(user_id, task.task_id, pool_id, expires_at)
            if not assignment:
                raise exc.AssignmentCreationError()
        return AssignmentOut.from_orm(assignment)

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> AssignmentOut:
        updated_assignment = self._assignment_repo.get_assignment_by_id(user_id, assignment_id)
        if not updated_assignment:
            raise exc.AssignmentNotFoundError()

        if updated_assignment.expires_at and timezone.now() > updated_assignment.expires_at:
            self._assignment_repo.reject_expired_assignment(updated_assignment.assignment_id)
            raise exc.AssignmentOperationError()

        if isinstance(annotation_data.annotation, list):
            updated_assignment.annotation = [item.model_dump() for item in annotation_data.annotation]
        else:
            updated_assignment.annotation = annotation_data.annotation.model_dump()

        updated_assignment.status = Assignment.Status.PENDING
        updated_assignment.completed_at = timezone.now()

        assignment = self._assignment_repo.update_assignment(updated_assignment)
        if not assignment:
            raise exc.AssignmentUpdatingError()

        self._pipeline_engine._evaluate_stage_completion(assignment.task_id, assignment.task.pool_id)

        return AssignmentOut.from_orm(assignment)
