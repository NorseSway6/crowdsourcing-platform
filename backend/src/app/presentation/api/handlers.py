from uuid import UUID

from ninja import UploadedFile

from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema
from app.domain.entities.dataset_schema import DatasetOut, DatasetSchema
from app.domain.entities.pipeline_schema import PipelineIn, PipelineOut
from app.domain.entities.platform_user_schema import UserOut, UserSchema
from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.skill_schema import SkillSchema
from app.domain.entities.task_schema import TaskOut
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.services.assignment_service import AssignmentService
from app.domain.services.dataset_service import DatasetService
from app.domain.services.pipeline_engine import PipelineEngine
from app.domain.services.platform_user_service import UserService
from app.domain.services.pool_service import PoolService
from app.domain.services.skill_service import SkillService
from app.domain.services.task_service import TaskService


class SkillHandlers:
    def __init__(self, skill_service: SkillService):
        self._skill_service = skill_service

    def get_all_skills(self, request) -> tuple[int, list[str] | ErrorResponse]:
        skills = self._skill_service.get_all_skills()
        if not skills:
            return 404, ErrorResponse(detail="Skills not found")
        return 200, skills

    def create_skill(self, request, skill_data: SkillSchema) -> tuple[int, SkillSchema | ErrorResponse]:
        skill = self._skill_service.create_skill(skill_data)
        if not skill:
            return 400, ErrorResponse(detail="Skills not found")
        return 201, skill

    def delete_skill(self, request, skill_data: SkillSchema) -> tuple[int, SuccessResponse | ErrorResponse]:
        deleted = self._skill_service.delete_skill(skill_data)
        if not deleted:
            return 400, ErrorResponse(detail="Skill delete error")
        return 200, SuccessResponse(detail="Skill delete successfully")


class PoolHandlers:
    def __init__(self, pool_service: PoolService):
        self._pool_service = pool_service

    def get_all_pools(self, request) -> tuple[int, list[PoolOut] | ErrorResponse]:
        pools = self._pool_service.get_all_pools()
        if not pools:
            return 404, ErrorResponse(detail="Pools not found")
        return 200, pools

    def get_pool_by_id(self, request, pool_id: int) -> tuple[int, PoolOut | ErrorResponse]:
        pool = self._pool_service.get_pool_by_id(pool_id)
        if not pool:
            return 404, ErrorResponse(detail="Pools not found")
        return 200, pool

    def update_pool(self, request, pool_id: int, pool_data: PoolSchema) -> tuple[int, PoolOut | ErrorResponse]:
        updated = self._pool_service.update_pool(pool_id, pool_data)
        if not updated:
            return 400, ErrorResponse(detail="Pool update error")
        return 200, updated


class PipelineHandlers:
    def __init__(self, pipeline_service: PipelineEngine):
        self._pipeline_service = pipeline_service

    def get_pipelines_by_user(self, request, owner_id: UUID) -> tuple[int, list[PipelineOut] | ErrorResponse]:
        pipelines = self._pipeline_service.get_pipelines_by_user(owner_id)
        if not pipelines:
            return 404, ErrorResponse(detail="Pipelines not found")
        return 200, pipelines

    def create_pipeline(
        self, request, owner_id: UUID, pipeline_data: PipelineIn
    ) -> tuple[int, PipelineOut | ErrorResponse]:
        pipeline = self._pipeline_service.create_pools(owner_id, pipeline_data)
        if not pipeline:
            return 400, ErrorResponse(detail="Pipeline create error")
        return 201, pipeline

    def update_pipeline(
        self, request, pipeline_id: int, pipeline_data: PipelineIn
    ) -> tuple[int, PipelineOut | ErrorResponse]:
        updated = self._pipeline_service.update_pipeline(pipeline_id, pipeline_data)
        if not updated:
            return 400, ErrorResponse(detail="Pipeline update error")
        return 200, updated

    def delete_pipeline(self, request, pipeline_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        deleted = self._pipeline_service.delete_pipeline(pipeline_id)
        if not deleted:
            return 400, ErrorResponse(detail="Pipeline delete error")
        return 200, SuccessResponse(detail="Pipeline delete successfully")


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def create_user(self, request, user_data: UserSchema) -> tuple[int, UserOut | ErrorResponse]:
        user = self._user_service.create_user(user_data)
        if not user:
            return 400, ErrorResponse(detail="User create error")
        return 201, user

    def get_all_users(self, request) -> tuple[int, list[UserOut] | ErrorResponse]:
        users = self._user_service.get_all_users()
        if not users:
            return 404, ErrorResponse(detail="Users not found")
        return 200, users

    def get_user_by_id(self, request, user_id: UUID) -> tuple[int, UserOut | ErrorResponse]:
        user = self._user_service.get_user_by_id(user_id)
        if not user:
            return 404, ErrorResponse(detail="User not found")
        return 200, user

    def update_user_profile(
        self, request, user_id: UUID, profile_data: ProfileSchema
    ) -> tuple[int, UserOut | ErrorResponse]:
        user = self._user_service.update_user_profile(user_id, profile_data)
        if not user:
            return 400, ErrorResponse(detail="User not found")
        return 200, user

    def delete_user(self, request, user_id: UUID) -> tuple[int, SuccessResponse | ErrorResponse]:
        deleted = self._user_service.delete_user(user_id)
        if not deleted:
            return 400, ErrorResponse(detail="User delete error")
        return 200, SuccessResponse(detail="User delete successfully")


class DatasetHandlers:
    def __init__(self, dataset_service: DatasetService):
        self._dataset_service = dataset_service

    def get_dataset_by_id(self, request, dataset_id: int) -> tuple[int, DatasetOut | ErrorResponse]:
        dataset = self._dataset_service.get_dataset_by_id(dataset_id)
        if not dataset:
            return 404, ErrorResponse(detail="Dataset not found")
        return 200, dataset

    def get_datasets_by_user(self, request, user_id: UUID) -> tuple[int, list[DatasetOut] | ErrorResponse]:
        datasets = self._dataset_service.get_datasets_by_user(user_id)
        if not datasets:
            return 404, ErrorResponse(detail="Datasets not found")
        return 200, datasets

    def create_dataset(
        self, request, owner_id: UUID, dataset_data: DatasetSchema
    ) -> tuple[int, DatasetOut | ErrorResponse]:
        dataset = self._dataset_service.create_dataset(owner_id, dataset_data)
        if not dataset:
            return 400, ErrorResponse(detail="Dataset create error")
        return 201, dataset

    def update_dataset(
        self, request, dataset_id: int, dataset_data: DatasetSchema
    ) -> tuple[int, DatasetOut | ErrorResponse]:
        updated = self._dataset_service.update_dataset(dataset_id, dataset_data)
        if not updated:
            return 400, ErrorResponse(detail="Dataset update error")
        return 200, updated

    def delete_dataset(self, request, dataset_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        deleted = self._dataset_service.delete_dataset(dataset_id)
        if not deleted:
            return 400, ErrorResponse(detail="Dataset delete error")
        return 200, SuccessResponse(detail="Dataset delete successfully")

    def upload_images(self, request, dataset_id: int, files: UploadedFile) -> tuple[int, list[TaskOut] | ErrorResponse]:
        dataset = self._dataset_service.upload_images(dataset_id, files)
        if not dataset:
            return 400, ErrorResponse(detail="Image upload error")
        return 201, dataset


class TaskHandlers:
    def __init__(self, task_service: TaskService):
        self._task_service = task_service

    def get_all_tasks(self, request) -> tuple[int, list[TaskOut] | ErrorResponse]:
        tasks = self._task_service.get_all_tasks()
        if not tasks:
            return 404, ErrorResponse(detail="Tasks not found")
        return 200, tasks

    def get_task_by_id(self, request, task_id: int) -> tuple[int, TaskOut | ErrorResponse]:
        task = self._task_service.get_task_by_id(task_id)
        if not task:
            return 404, ErrorResponse(detail="Task not found")
        return 200, task

    def delete_task(self, request, task_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        deleted = self._task_service.delete_task(task_id)
        if not deleted:
            return 400, ErrorResponse(detail="Task delete error")
        return 200, SuccessResponse(detail="Task delete successfully")


class AssignmentHandlers:
    def __init__(self, assignment_service: AssignmentService):
        self._assignment_service = assignment_service

    def get_assignments_by_user(self, request, user_id: UUID) -> tuple[int, list[AssignmentOut] | ErrorResponse]:
        assignments = self._assignment_service.get_assignments_by_user(user_id)
        if not assignments:
            return 404, ErrorResponse(detail="Assignments not found")
        return 200, assignments

    def create_assignment(self, request, user_id: UUID, pool_id: int) -> tuple[int, AssignmentOut | ErrorResponse]:
        assignment = self._assignment_service.create_assignment(user_id, pool_id)
        if not assignment:
            return 400, ErrorResponse(detail="Assignment create error")
        return 201, assignment

    def update_assignment(
        self, request, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema
    ) -> tuple[int, AssignmentOut | ErrorResponse]:
        updated = self._assignment_service.update_assignment(user_id, assignment_id, annotation_data)
        if not updated:
            return 400, ErrorResponse(detail="Assignment update error")
        return 200, updated
