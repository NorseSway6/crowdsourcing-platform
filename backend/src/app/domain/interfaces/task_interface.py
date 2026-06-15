from uuid import UUID

from app.db.models.task import Task


class ITaskRepository:
    def get_all_tasks(self) -> list[Task]:
        pass

    def get_task_by_id(self, task_id: int) -> Task:
        pass

    def bulk_create_task(self, tasks_to_create: list[Task]) -> Task:
        pass

    def delete_task(self, task_id: int) -> bool:
        pass

    def get_unassigned_tasks_by_dataset(self, dataset_id: int) -> list[Task]:
        pass

    def link_tasks_to_pool(self, tasks_ids: list[int], pool_id: int) -> bool:
        pass

    def get_next_task(self, user_id: UUID, pool_id: int) -> Task:
        pass

    def _mark_task_completed(self, task_id: int, pool_id: int) -> bool:
        pass

    def _move_task_to_pool(self, task_id: int, new_pool_id: int, intermediate_data: dict) -> bool:
        pass

    def count_unfinished_tasks(self, pool_id: int) -> int:
        pass

    def get_completed_tasks_annotations(self, dataset_id: int) -> list[dict[str, any]]:
        pass
