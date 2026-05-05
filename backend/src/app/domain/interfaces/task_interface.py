from typing import List
from uuid import UUID

from app.domain.entities.task_schema import TaskOut, TaskSchema


class ITaskRepository:
    def get_all_tasks(self) -> List[TaskOut]:
        pass

    def get_task_by_id(self, task_id: int) -> TaskOut:
        pass

    def create_task(self, pool_id: int, user_id: UUID, task_data: dict) -> TaskOut:
        pass
