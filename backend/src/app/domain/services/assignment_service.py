from typing import List
from uuid import UUID

from django.utils import timezone

from app.db.models.assignments import Assignment
from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.interfaces.assignment_interface import IAssignmentRepository
from app.domain.interfaces.task_interface import ITaskRepository


class AssignmentService:
    def __init__(self, assignment_repo: IAssignmentRepository, task_repo: ITaskRepository):
        self._assignment_repo = assignment_repo
        self._task_repo = task_repo

    def get_all_assignments(self) -> List[AssignmentOut]:
        assignments = self._assignment_repo.get_all_assignments()
        if not assignments:
            return None
        return [AssignmentOut.from_orm(a) for a in assignments]

    def get_assignments_by_user(self, user_id: UUID) -> List[AssignmentOut]:
        assignments = self._assignment_repo.get_assignments_by_user(user_id)
        if not assignments:
            return None
        return [AssignmentOut.from_orm(a) for a in assignments]

    def create_assignment(self, user_id: UUID) -> AssignmentOut:
        assignmented_task = self._assignment_repo.get_active_assignment(user_id)
        if assignmented_task:
            return AssignmentOut.from_orm(assignmented_task)

        task = self._task_repo.get_next_task(user_id)
        if not task:
            return None

        assignment = self._assignment_repo.create_assignment(user_id, task.task_id)
        if not assignment:
            return None
        return AssignmentOut.from_orm(assignment)

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> AssignmentOut:
        updated_assignment = self._assignment_repo.get_assignment_by_id(user_id, assignment_id)
        if not updated_assignment:
            return None

        updated_assignment.annotation = [item.dict() for item in annotation_data.annotation]
        updated_assignment.status = Assignment.Status.PENDING
        updated_assignment.completed_at = timezone.now()

        assignment = self._assignment_repo.update_assignment(updated_assignment)
        return AssignmentOut.from_orm(assignment)

    def update_assignment_status(self, user_id: UUID, assignment_id: int, status: str) -> AssignmentOut:
        updated_assignment = self._assignment_repo.get_assignment_by_id(user_id, assignment_id)
        if not updated_assignment:
            return None

        updated_assignment.status = status

        assignment = self._assignment_repo.update_assignment(updated_assignment)
        return AssignmentOut.from_orm(assignment)
