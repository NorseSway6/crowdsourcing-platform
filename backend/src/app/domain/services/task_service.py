from typing import List

from app.db.models.pool import Pool
from app.domain.entities.task_schema import TaskOut
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.task_interface import ITaskRepository


class TaskService:
    def __init__(self, task_repo: ITaskRepository, pool_repo: IPoolRepository):
        self._task_repo = task_repo
        self._pool_repo = pool_repo

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

    def _move_task_to_annotation_retry(self, task_id: int, current_pool_id: int) -> bool:
        current_pool = self._pool_repo.get_pool_by_id(current_pool_id)
        if not current_pool:
            return None

        annotation_pool = self._pool_repo._get_pool_by_type(
            pipeline_id=current_pool.pipeline_id, pool_type=Pool.PoolType.ANNOTATION
        )
        if not annotation_pool:
            return None

        moved = self._task_repo._move_task_to_pool(
            task_id=task_id, new_pool_id=annotation_pool.pool_id, intermediate_data={}
        )
        if not moved:
            return None

        marked = None
        if annotation_pool.status == Pool.PoolStatus.COMPLETED:
            marked = self._pool_repo._mark_pool_open(annotation_pool.pool_id)
            if not marked:
                return None

        return marked

    def link_tasks_to_pool(self, tasks: List[TaskOut], pool_id: int, limit: int) -> bool:
        if limit is None or limit <= 0:
            task_ids = [t.task_id for t in tasks]
        else:
            task_ids = [t.task_id for t in tasks][:limit]

        return self._task_repo.link_tasks_to_pool(task_ids, pool_id)
