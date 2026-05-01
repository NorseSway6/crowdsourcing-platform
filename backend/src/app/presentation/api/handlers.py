from typing import List
from uuid import UUID

from ninja import Body, Path

from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.skill_schema import SkillSchema
from app.domain.entities.task_schema import TaskOut, TaskSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.services.dataset_service import DatasetService
from app.domain.services.platform_user_service import UserService
from app.domain.services.pool_service import PoolService
from app.domain.services.skill_service import SkillService
from app.domain.services.task_service import TaskService


class SkillHandlers:
    def __init__(self, skill_service: SkillService):
        self._skill_service = skill_service

    def get_all_skills(self, request) -> List[SkillSchema]:
        return self._skill_service.get_all_skills()


class PoolHandlers:
    def __init__(self, pool_service: PoolService):
        self._pool_service = pool_service

    def get_all_pools(self, request) -> List[PoolOut]:
        return self._pool_service.get_all_pools()

    def get_pool_by_id(self, request, pool_id: int) -> PoolOut:
        return self._pool_service.get_pool_by_id(pool_id)

    def create_pool(self, request, pool_data: PoolSchema) -> PoolOut:
        return self._pool_service.create_pool(pool_data)

    def update_pool(self, request, pool_id: int, pool_data: PoolSchema) -> PoolSchema:
        return self._pool_service.update_pool(pool_id, pool_data)

    def create_task(self, request, pool_id: int, task_data: TaskSchema) -> TaskOut:
        return self._pool_service.create_task(pool_id, task_data)


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def get_or_create_user(self, request, user_data: UserIn = Body(...)) -> UserOut:
        return self._user_service.get_or_create_user(user_data)

    def get_all_users(self, request) -> List[UserOut]:
        return self._user_service.get_all_users()

    def get_user_by_id(self, request, user_id: UUID = Path(...)):
        return self._user_service.get_user_by_id(user_id)

    def update_user_profile(self, request, user_id: UUID, profile_data: ProfileSchema) -> UserOut:
        return self._user_service.update_user_profile(user_id, profile_data)


class DatasetHandlers:
    def __init__(self, dataset_service: DatasetService):
        self._dataset_service = dataset_service

    def get_all_datasets(self, request) -> List[DatasetOut]:
        return self._dataset_service.get_all_datasets()

    def get_dataset_by_id(self, request, dataset_id: int) -> DatasetOut:
        return self._dataset_service.get_dataset_by_id(dataset_id)

    def create_dataset(self, request, owner_id: UUID, dataset_data: DatasetSchema) -> DatasetOut:
        return self._dataset_service.create_dataset(owner_id, dataset_data)

    def update_dataset(self, request, dataset_id: int, dataset_data: DatasetSchema) -> DatasetOut:
        return self._dataset_service.update_dataset(dataset_id, dataset_data)


class TaskHandlers:
    def __init__(self, task_service: TaskService):
        self._task_service = task_service

    def get_all_tasks(self, request) -> List[TaskOut]:
        return self._task_service.get_all_tasks()

    def get_task_by_id(self, request, task_id: int) -> TaskOut:
        return self._task_service.get_task_by_id(task_id)
