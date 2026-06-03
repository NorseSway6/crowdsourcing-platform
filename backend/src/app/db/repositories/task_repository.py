from uuid import UUID

from django.db.models import Count, F, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce

from app.db.models.assignments import Assignment
from app.db.models.pool import Pool
from app.db.models.task import Task
from app.domain.interfaces.task_interface import ITaskRepository


class TaskRepository(ITaskRepository):
    def get_all_tasks(self) -> list[Task]:
        tasks = Task.objects.all()
        return tasks

    def get_task_by_id(self, task_id: int) -> Task:
        return Task.objects.filter(task_id=task_id).first()

    def delete_task(self, task_id: int) -> bool:
        deleted, _ = Task.objects.filter(task_id=task_id).delete()
        return deleted

    def get_unassigned_tasks_by_dataset(self, dataset_id: int) -> list[Task]:
        return Task.objects.filter(dataset_id=dataset_id, pool_id__isnull=True).all()

    def link_tasks_to_pool(self, tasks_ids: list[int], pool_id: int) -> bool:
        updated = Task.objects.filter(task_id__in=tasks_ids).update(pool_id=pool_id)
        return updated > 0

    def get_next_task(self, user_id: UUID, pool_id: int) -> Task | None:
        valid_assignments_subquery = (
            Assignment.objects.filter(
                task_id=OuterRef("pk"),
                pool_id=pool_id,
            )
            .exclude(status__in=[Assignment.Status.REJECTED, Assignment.Status.ARCHIVED])
            .values("task_id")
            .annotate(cnt=Count("assignment_id"))
            .values("cnt")
        )

        candidate_id = (
            Task.objects.filter(
                pool_id=pool_id,
                pool__status=Pool.PoolStatus.OPEN,
            )
            .filter(Q(pool__skills__isnull=True) | Q(pool__skills__profile_skill__user_id=user_id))
            .exclude(assignment_task__user_id=user_id)
            .annotate(valid_assignments_count=Coalesce(Subquery(valid_assignments_subquery), 0))
            .filter(valid_assignments_count__lt=F("pool__overlap"))
            .order_by("pk")
            .values_list("pk", flat=True)
            .first()
        )
        if not candidate_id:
            return None

        return Task.objects.select_for_update(skip_locked=True).filter(pk=candidate_id).first()

    def _mark_task_completed(
        self,
        task_id: int,
        pool_id: int,
    ) -> bool:
        updated = Task.objects.filter(task_id=task_id, pool_id=pool_id).update(status=Task.Status.COMPLETED)
        return updated > 0

    def _move_task_to_pool(self, task_id: int, new_pool_id: int, intermediate_data: dict) -> bool:
        updated = Task.objects.filter(task_id=task_id).update(
            pool_id=new_pool_id,
            status=Task.Status.AVAILABLE,
            annotation=intermediate_data,
        )
        return updated > 0

    def count_unfinished_tasks(self, pool_id: int) -> int:
        return (
            Task.objects.filter(pool_id=pool_id)
            .exclude(assignment_task__pool_id=pool_id, assignment_task__status=Assignment.Status.APPROVED)
            .count()
        )

    def get_completed_tasks_annotations(self, dataset_id: int) -> list[dict[str, any]]:
        return list(
            Task.objects.filter(dataset_id=dataset_id, status=Task.Status.COMPLETED).values(
                "task_id", "image", "annotation", "width", "height"
            )
        )
