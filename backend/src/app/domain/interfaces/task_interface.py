from typing import List
from uuid import UUID

from app.db.models.task import Task
from app.domain.entities.task_schema import TaskOut, TaskSchema


class ITaskRepository:
    def get_all_tasks(self) -> List[TaskOut]:
        pass

    def get_task_by_id(self, task_id: int) -> TaskOut:
        pass

    def delete_task(self, task_id: int) -> bool:
        pass

    def get_next_task(self, pool_id: int, datas: List[int]) -> Task:
        pass
