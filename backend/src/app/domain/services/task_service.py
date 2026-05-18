from typing import List
from uuid import UUID

from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.domain.interfaces.task_interface import ITaskRepository


class TaskService:
    def __init__(self, task_repo: ITaskRepository):
        self._task_repo = task_repo

    def get_all_tasks(self) -> List[TaskOut]:
        tasks = self._task_repo.get_all_tasks()
        if not tasks:
            return None
        return [TaskOut.from_orm(t) for t in tasks]

    def get_task_by_id(self, task_id: int) -> TaskOut:
        task = self._task_repo.get_task_by_id(task_id)
        if not task:
            return None
        return TaskOut.from_orm(task)

    def delete_task(self, task_id: int) -> bool:
        deleted = self._task_repo.delete_task(task_id)
        if not deleted:
            return None

        return deleted
