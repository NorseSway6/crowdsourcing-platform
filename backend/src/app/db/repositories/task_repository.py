from typing import List
from uuid import UUID

from django.db.models import Count, F, Q

from app.db.models.assignments import Assignment
from app.db.models.task import Task
from app.domain.interfaces.task_interface import ITaskRepository


class TaskRepository(ITaskRepository):
    def get_all_tasks(self) -> List[Task]:
        tasks = Task.objects.all()
        return tasks

    def get_task_by_id(self, task_id: int) -> Task:
        return Task.objects.filter(task_id=task_id).first()

    def delete_task(self, task_id: int) -> bool:
        deleted, _ = Task.objects.filter(task_id=task_id).delete()
        return deleted

    def get_next_task(self, user_id: UUID) -> Task:
        return (
            Task.objects.filter(pool__is_active=True, pool__skills__profile_skill__user_id=user_id)
            .exclude(assignment_task__user_id=user_id)
            .annotate(
                valid_assignments_count=Count(
                    "assignment_task",
                    filter=Q(assignment_task__status__in=[Assignment.Status.PENDING, Assignment.Status.APPROVED]),
                )
            )
            .filter(valid_assignments_count__lt=F("pool__overlap"))
            .distinct()
            .first()
        )
