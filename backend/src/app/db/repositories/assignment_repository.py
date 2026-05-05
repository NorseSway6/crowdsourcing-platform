from typing import List
from uuid import UUID

from django.db.models import Count, F
from django.utils import timezone

from app.db.models.assignments import Assignment
from app.db.models.task import Task
from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.interfaces.assignment_interface import IAssignmentRepository


class AssignmentRepository(IAssignmentRepository):
    def get_all_assignments(self) -> List[AssignmentOut]:
        return list(Assignment.objects.filter().all())

    def get_assignment_tasks(self, user_id: UUID) -> List[AssignmentOut]:
        return list(Assignment.objects.filter(user_id=user_id).all())

    def create_assignment(self, user_id: UUID, pool_id: int) -> AssignmentOut:
        user_assigned_tasks = Assignment.objects.filter(user_id=user_id).values_list("task_id", flat=True)

        task = (
            Task.objects.filter(pool_id=pool_id)
            .exclude(task_id__in=user_assigned_tasks)
            .annotate(assign_count=Count("assignment_task"))
            .filter(assign_count__lt=F("pool__overlap"))
            .first()
        )

        assignment = Assignment.objects.create(task_id=task.task_id, user_id=user_id)

        return assignment

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> AssignmentOut:
        assignment = Assignment.objects.get(assignment_id=assignment_id, user_id=user_id)

        assignment.annotation = annotation_data.annotation
        assignment.status = Assignment.Status.PENDING
        assignment.completed_at = timezone.now()
        assignment.save()

        return assignment

    def update_assignment_status(self, user_id: UUID, assignment_id: int, status: str) -> AssignmentOut:
        assignment = Assignment.objects.get(assignment_id=assignment_id, user_id=user_id)

        assignment.status = status
        assignment.save()

        return assignment
