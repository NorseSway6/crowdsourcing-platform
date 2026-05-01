from typing import List

from app.db.models.task import Task
from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.domain.interfaces.task_interface import ITaskRepository


class TaskRepository(ITaskRepository):
    def get_all_tasks(self) -> List[TaskOut]:
        return Task.objects.all()

    def get_task_by_id(self, task_id: int) -> TaskOut:
        return Task.objects.filter(task_id=task_id).first()
