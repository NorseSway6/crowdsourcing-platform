from typing import List
from uuid import UUID

from ninja.errors import HttpError

from app.db.models.task import Task
from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.domain.interfaces.task_interface import ITaskRepository


class TaskRepository(ITaskRepository):
    def get_all_tasks(self) -> List[TaskOut]:
        tasks = Task.objects.all()
        if not tasks:
            raise HttpError(404, "Tasks not found")
        return [TaskOut.from_orm(t) for t in tasks]

    def get_task_by_id(self, task_id: int) -> TaskOut:
        task = Task.objects.filter(task_id=task_id).first()
        if task is None:
            raise HttpError(404, "Task not found")
        return TaskOut.from_orm(task)

    def delete_task(self, task_id: int) -> bool:
        deleted, _ = Task.objects.filter(task_id=task_id).delete()
        if not deleted:
            raise HttpError(404, "Task for delete not found")
        return deleted
