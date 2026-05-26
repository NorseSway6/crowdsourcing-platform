from uuid import UUID

from django.db import IntegrityError

from app.db.models.assignments import Assignment
from app.domain.interfaces.assignment_interface import IAssignmentRepository


class AssignmentRepository(IAssignmentRepository):
    def get_assignments_by_user(self, user_id: UUID) -> list[Assignment]:
        return list(Assignment.objects.filter(user_id=user_id))

    def get_assignment_by_id(self, user_id: UUID, assignment_id: int) -> Assignment:
        return Assignment.objects.select_related("task").filter(assignment_id=assignment_id, user_id=user_id).first()

    def create_assignment(self, user_id: UUID, task_id: int, pool_id: int) -> Assignment:
        try:
            assignment = Assignment.objects.create(task_id=task_id, user_id=user_id, pool_id=pool_id)
        except IntegrityError:
            return None

        return assignment

    def update_assignment(self, data: Assignment) -> Assignment:
        try:
            data.save()
        except Exception:
            return None

        return data

    def _get_active_assignment(self, user_id: UUID) -> Assignment:
        return Assignment.objects.filter(user_id=user_id, status=Assignment.Status.IN_PROGRESS).first()

    def _get_completed_annotations(self, task_id: int, pool_id: int) -> list[dict]:
        return list(
            Assignment.objects.filter(
                task_id=task_id,
                task__pool_id=pool_id,
                status__in=[Assignment.Status.PENDING, Assignment.Status.APPROVED],
            )
            .exclude(annotation__isnull=True)
            .values_list("annotation", flat=True)
        )

    def _get_all_for_task(self, task_id: int, current_pool_id: int) -> list[Assignment]:
        return Assignment.objects.filter(task_id=task_id, task__pool_id=current_pool_id).all()

    def _bulk_update_assignments(self, assignments: list[Assignment]) -> None:
        Assignment.objects.bulk_update(assignments, ["status"])
