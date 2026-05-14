from typing import List
from uuid import UUID

from django.db.models import Count, F
from django.utils import timezone
from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.assignments import Assignment
from app.db.models.task import Task
from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.interfaces.assignment_interface import IAssignmentRepository


class AssignmentRepository(IAssignmentRepository):
    def get_all_assignments(self) -> List[AssignmentOut]:
        assignments = Assignment.objects.all()
        if not assignments:
            raise HttpError(404, "Assignments not found")
        return [AssignmentOut.from_orm(a) for a in assignments]

    def get_assignments_by_user(self, user_id: UUID) -> List[AssignmentOut]:
        assignments = Assignment.objects.filter(user_id=user_id).all()
        if not assignments:
            raise HttpError(404, "Assignments not found")
        return [AssignmentOut.from_orm(a) for a in assignments]

    def create_assignment(self, user_id: UUID, pool_id: int) -> AssignmentOut:
        user_assigned_tasks = Assignment.objects.filter(user_id=user_id).values_list("task_id", flat=True)

        task = (
            Task.objects.filter(pool_id=pool_id)
            .exclude(task_id__in=user_assigned_tasks)
            .annotate(assign_count=Count("assignment_task"))
            .filter(assign_count__lt=F("pool__overlap"))
            .first()
        )
        if task is None:
            raise HttpError(404, "Task not found")

        try:
            assignment = Assignment.objects.create(task_id=task.task_id, user_id=user_id)
        except IntegrityError:
            raise HttpError(409, "Create failed due to integrity error")

        return AssignmentOut.from_orm(assignment)

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> AssignmentOut:
        assignment = Assignment.objects.filter(assignment_id=assignment_id, user_id=user_id).first()
        if assignment is None:
            raise HttpError(404, "Assignment or user not found")

        assignment.annotation = [item.dict() for item in annotation_data.annotation]
        assignment.status = Assignment.Status.PENDING
        assignment.completed_at = timezone.now()

        try:
            assignment.save()
        except Exception:
            return HttpError(409, "Update failed due to save error")

        return AssignmentOut.from_orm(assignment)

    def update_assignment_status(self, user_id: UUID, assignment_id: int, status: str) -> AssignmentOut:
        assignment = Assignment.objects.filter(assignment_id=assignment_id, user_id=user_id).first()
        if assignment is None:
            raise HttpError(404, "Assignment or user not found")

        assignment.status = status

        try:
            assignment.save()
        except Exception:
            return HttpError(409, "Update failed due to save error")

        return AssignmentOut.from_orm(assignment)
