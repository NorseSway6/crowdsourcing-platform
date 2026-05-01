from typing import List

from app.domain.entities.task_schema import TaskOut, TaskSchema


class ITaskRepository:
    def get_all_tasks(self) -> List[TaskOut]:
        pass

    def get_task_by_id(self, task_id: int) -> TaskOut:
        pass
