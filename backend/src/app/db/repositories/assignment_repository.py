from typing import List
from uuid import UUID

from django.db import IntegrityError

from app.db.models.assignments import Assignment
from app.db.models.task import Task
from app.domain.interfaces.assignment_interface import IAssignmentRepository


class AssignmentRepository(IAssignmentRepository):
    def get_all_assignments(self) -> List[Assignment]:
        return list(Assignment.objects.all())

    def get_assignments_by_user(self, user_id: UUID) -> List[Assignment]:
        return list(Assignment.objects.filter(user_id=user_id))

    def get_assignment_by_id(self, user_id: UUID, assignment_id: int) -> Assignment:
        return Assignment.objects.filter(assignment_id=assignment_id, user_id=user_id).first()

    def create_assignment(self, user_id: UUID, task_id: int) -> Assignment:
        try:
            assignment = Assignment.objects.create(task_id=task_id, user_id=user_id)
        except IntegrityError:
            return None

        return assignment

    def update_assignment(self, data: Assignment) -> Assignment:
        try:
            data.save()
        except Exception:
            return None

        return data

    def get_active_assignment(self, user_id: UUID) -> Assignment:
        return Assignment.objects.filter(user_id=user_id, status=Assignment.Status.IN_PROGRESS).first()
