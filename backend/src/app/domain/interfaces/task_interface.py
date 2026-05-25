from typing import List
from uuid import UUID

from app.db.models.task import Task
from app.domain.entities.task_schema import TaskOut


class ITaskRepository:
    def get_all_tasks(self) -> List[TaskOut]:
        pass

    def get_task_by_id(self, task_id: int) -> TaskOut:
        pass

    def delete_task(self, task_id: int) -> bool:
        pass

    def get_unassigned_tasks_by_dataset(self, dataset_id: int) -> any:
        pass

    def link_tasks_to_pool(self, tasks_queryset, pool_id: int, limit: int | None = None) -> None:
        pass

    def get_next_task(self, user_id: UUID) -> Task:
        pass

    def _mark_task_completed(self, task_id: int, final_annotation: List) -> None:
        pass

    def _move_task_to_pool(self, task_id: int, new_pool_id: int, intermediate_data: dict) -> None:
        pass
