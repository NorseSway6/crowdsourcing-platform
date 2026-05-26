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

    def get_unassigned_tasks_by_dataset(self, dataset_id: int) -> any:
        return Task.objects.filter(dataset_id=dataset_id, pool_id__isnull=True)

    def link_tasks_to_pool(self, tasks_queryset, pool_id: int, limit: int | None = None) -> None:
        if limit is not None and limit > 0:
            task_ids = list(tasks_queryset.values_list("task_id", flat=True)[:limit])
            Task.objects.filter(task_id__in=task_ids).update(pool_id=pool_id)
        else:
            tasks_queryset.update(pool_id=pool_id)

    def get_next_task(self, user_id: UUID, pool_id: int) -> Task | None:
        # 1. Подзапрос: считаем валидные решения ЭТОЙ задачи ТОЛЬКО в ТЕКУЩЕМ пулле
        valid_assignments_subquery = (
            Assignment.objects.filter(
                task_id=OuterRef("pk"),
                pool_id=pool_id,  # Считаем только решения из нового этапа!
            )
            .exclude(status=Assignment.Status.REJECTED)
            .values("task_id")
            .annotate(cnt=Count("assignment_id"))
            .values("cnt")
        )

        # 2. Основной запрос
        candidate_id = (
            Task.objects.filter(
                pool_id=pool_id,
                pool__status=Pool.PoolStatus.OPEN,
                pool__skills__profile_skill__user_id=user_id,
            )
            # Исключаем юзера, если он делал эту задачу на ЛЮБОМ этапе истории
            .exclude(assignment_task__user_id=user_id)
            # Подключаем изолированный счетчик решений текущего этапа
            .annotate(valid_assignments_count=Coalesce(Subquery(valid_assignments_subquery), 0))
            # Теперь фильтр работает только для текущего пулла!
            .filter(valid_assignments_count__lt=F("pool__overlap"))
            .order_by("pk")
            .values_list("pk", flat=True)
            .first()
        )

        if not candidate_id:
            return None

        # 3. Атомарный лок
        return Task.objects.select_for_update(skip_locked=True).filter(pk=candidate_id).first()

    def _mark_task_completed(self, task_id: int, final_annotation: list) -> None:
        Task.objects.filter(task_id=task_id).update(status=Task.Status.COMPLETED, annotation=final_annotation)

    def _move_task_to_pool(self, task_id: int, new_pool_id: int, intermediate_data: dict) -> None:
        Task.objects.filter(task_id=task_id).update(
            pool_id=new_pool_id,
            status=Task.Status.AVAILABLE,
            annotation=intermediate_data,
        )
