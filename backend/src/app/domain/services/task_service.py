from typing import List
from uuid import UUID

from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.domain.interfaces.task_interface import ITaskRepository


class TaskService:
    def __init__(self, task_repo: ITaskRepository):
        self._task_repo = task_repo

    def get_all_tasks(self) -> List[TaskOut]:
        return self._task_repo.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> TaskOut:
        return self._task_repo.get_task_by_id(task_id)

    def delete_task(self, task_id: int) -> bool:
        return self._task_repo.delete_task(task_id)
