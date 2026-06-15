from http import HTTPStatus
from uuid import UUID

from celery.result import AsyncResult
from django_redis import get_redis_connection
from ninja import UploadedFile

from app.domain.entities.anallytics_schema import PoolProgressOut, PoolsProgressFilter, UserInfoFilter, UserInfoOut
from app.domain.entities.assigment_schema import AssignmentActiveOut, AssignmentHistoryOut, AssignmentSchema
from app.domain.entities.auth_schema import LogIn, RefreshTokenIn, TokenOut
from app.domain.entities.dataset_schema import CategoryOut, CategorySchema, DatasetOut, DatasetSchema
from app.domain.entities.export_schema import ExportStatusOut, UploadStatusOut
from app.domain.entities.pipeline_schema import PipelineIn, PipelineOut
from app.domain.entities.platform_user_schema import RegisterOut, RegisterSchema, UserOut, UserSchema
from app.domain.entities.pool_schema import (
    PoolDetailOut,
    PoolFilter,
    PoolInstructionOut,
    PoolInstructionSchema,
    PoolOut,
    PoolSchema,
)
from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.skill_schema import SkillSchema
from app.domain.entities.task_schema import TaskOut
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.services.analytics_module import AnalyticsService
from app.domain.services.assignment_service import AssignmentService
from app.domain.services.auth_service import AuthService
from app.domain.services.celery_tasks import run_dataset_export_task
from app.domain.services.dataset_service import DatasetService
from app.domain.services.export_service import ExportService
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
        return HTTPStatus.OK, skills

    def create_skill(self, request, skill_data: SkillSchema) -> tuple[int, SkillSchema | ErrorResponse]:
        skill = self._skill_service.create_skill(skill_data)
        return HTTPStatus.CREATED, skill

    def delete_skill(self, request, skill_data: SkillSchema) -> tuple[int, SuccessResponse | ErrorResponse]:
        self._skill_service.delete_skill(skill_data)
        return HTTPStatus.OK, SuccessResponse(detail="Skill delete successfully")


class PoolHandlers:
    def __init__(self, pool_service: PoolService):
        self._pool_service = pool_service

    def get_all_pools(self, request, filters: PoolFilter) -> tuple[int, list[PoolOut] | ErrorResponse]:
        pools = self._pool_service.get_all_pools(filters)
        return HTTPStatus.OK, pools

    def get_pool_by_id(self, request, pool_id: int) -> tuple[int, PoolOut | ErrorResponse]:
        pool = self._pool_service.get_pool_by_id(pool_id)
        return HTTPStatus.OK, pool

    def update_pool(self, request, pool_id: int, pool_data: PoolSchema) -> tuple[int, PoolOut | ErrorResponse]:
        updated = self._pool_service.update_pool(pool_id, pool_data)
        return HTTPStatus.OK, updated

    def create_instruction(
        self, request, pool_id: int, instruction: PoolInstructionSchema
    ) -> tuple[int, PoolDetailOut | ErrorResponse]:
        created = self._pool_service.create_instruction(pool_id, instruction)
        return HTTPStatus.CREATED, created

    def get_instruction_by_id(self, request, instruction_id: int) -> tuple[int, PoolInstructionOut | ErrorResponse]:
        instruction = self._pool_service.get_instruction_by_id(instruction_id)
        return HTTPStatus.OK, instruction

    def get_instruction_by_pool(self, request, pool_id: int) -> tuple[int, PoolInstructionOut | ErrorResponse]:
        instruction = self._pool_service.get_instruction_by_pool(pool_id)
        return HTTPStatus.OK, instruction


class PipelineHandlers:
    def __init__(self, pipeline_service: PipelineEngine):
        self._pipeline_service = pipeline_service

    def get_pipelines_by_user(self, request, owner_id: UUID) -> tuple[int, list[PipelineOut] | ErrorResponse]:
        pipelines = self._pipeline_service.get_pipelines_by_user(owner_id)
        return HTTPStatus.OK, pipelines

    def create_pipeline(
        self, request, owner_id: UUID, pipeline_data: PipelineIn
    ) -> tuple[int, PipelineOut | ErrorResponse]:
        pipeline = self._pipeline_service.create_pools(owner_id, pipeline_data)
        return HTTPStatus.CREATED, pipeline

    def update_pipeline(
        self, request, pipeline_id: int, pipeline_data: PipelineIn
    ) -> tuple[int, PipelineOut | ErrorResponse]:
        updated = self._pipeline_service.update_pipeline(pipeline_id, pipeline_data)
        return HTTPStatus.OK, updated

    def delete_pipeline(self, request, pipeline_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        self._pipeline_service.delete_pipeline(pipeline_id)
        return HTTPStatus.OK, SuccessResponse(detail="Pipeline delete successfully")


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def create_user(self, request, user_data: UserSchema) -> tuple[int, UserOut | ErrorResponse]:
        user = self._user_service.create_user(user_data)
        return HTTPStatus.CREATED, user

    def get_all_users(self, request) -> tuple[int, list[UserOut] | ErrorResponse]:
        users = self._user_service.get_all_users()
        return HTTPStatus.OK, users

    def get_user_by_id(self, request, user_id: UUID) -> tuple[int, UserOut | ErrorResponse]:
        user = self._user_service.get_user_by_id(user_id)
        return HTTPStatus.OK, user

    def update_user_profile(
        self, request, user_id: UUID, profile_data: ProfileSchema
    ) -> tuple[int, UserOut | ErrorResponse]:
        user = self._user_service.update_user_profile(user_id, profile_data)
        return HTTPStatus.OK, user

    def delete_user(self, request, user_id: UUID) -> tuple[int, SuccessResponse | ErrorResponse]:
        self._user_service.delete_user(user_id)
        return HTTPStatus.OK, SuccessResponse(detail="User delete successfully")


class DatasetHandlers:
    def __init__(self, dataset_service: DatasetService, export_service: ExportService):
        self._dataset_service = dataset_service
        self._export_service = export_service

    def get_dataset_by_id(self, request, dataset_id: int) -> tuple[int, DatasetOut | ErrorResponse]:
        dataset = self._dataset_service.get_dataset_by_id(dataset_id)
        return HTTPStatus.OK, dataset

    def get_datasets_by_user(self, request, user_id: UUID) -> tuple[int, list[DatasetOut] | ErrorResponse]:
        datasets = self._dataset_service.get_datasets_by_user(user_id)
        return HTTPStatus.OK, datasets

    def create_dataset(
        self, request, owner_id: UUID, dataset_data: DatasetSchema
    ) -> tuple[int, DatasetOut | ErrorResponse]:
        dataset = self._dataset_service.create_dataset(owner_id, dataset_data)
        return HTTPStatus.CREATED, dataset

    def update_dataset(
        self, request, dataset_id: int, dataset_data: DatasetSchema
    ) -> tuple[int, DatasetOut | ErrorResponse]:
        updated = self._dataset_service.update_dataset(dataset_id, dataset_data)
        return HTTPStatus.OK, updated

    def delete_dataset(self, request, dataset_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        self._dataset_service.delete_dataset(dataset_id)
        return HTTPStatus.OK, SuccessResponse(detail="Dataset delete successfully")

    def upload_images(
        self, request, dataset_id: int, files: list[UploadedFile]
    ) -> tuple[int, SuccessResponse | ErrorResponse]:
        job_id = self._dataset_service.upload_images(dataset_id, files)
        job_result = AsyncResult(job_id)

        response_data = {
            "job_id": job_id,
            "status": job_result.status,
        }

        return HTTPStatus.ACCEPTED, UploadStatusOut.from_orm(response_data)

    def upload_video(self, request, dataset_id: int, file: UploadedFile) -> tuple[int, SuccessResponse | ErrorResponse]:
        job_id = self._dataset_service.upload_video(dataset_id, file)
        job_result = AsyncResult(job_id)

        response_data = {
            "job_id": job_id,
            "status": job_result.status,
        }

        return HTTPStatus.ACCEPTED, UploadStatusOut.from_orm(response_data)

    def get_upload_status(self, request, job_id: str) -> tuple[int, UploadStatusOut | ErrorResponse]:
        job_result = AsyncResult(job_id)

        response_data = {
            "job_id": job_id,
            "status": job_result.status,
        }

        if job_result.status == "SUCCESS":
            response_data["created_count"] = job_result.result

        elif job_result.status == "FAILURE":
            return HTTPStatus.BAD_REQUEST, ErrorResponse(error_code="upload_status_error", detail=str(job_result.info))

        return HTTPStatus.OK, UploadStatusOut.from_orm(response_data)

    def export_dataset(self, request, dataset_id: int, format_type: str) -> tuple[int, SuccessResponse | ErrorResponse]:
        redis_client = get_redis_connection("default")
        lock_key = f"export_lock:dataset:{dataset_id}"  # noqa: E231

        is_locked = redis_client.set(lock_key, "processing", ex=600, nx=True)

        if not is_locked:
            return HTTPStatus.CONFLICT, ErrorResponse(error_code="export_error", detail="Error is already started")

        job = run_dataset_export_task.delay(dataset_id, format_type)
        job_result = AsyncResult(job.id)

        response_data = {
            "job_id": job.id,
            "status": job_result.status,
        }

        return HTTPStatus.ACCEPTED, ExportStatusOut.from_orm(response_data)

    def get_export_status(self, request, job_id: str) -> tuple[int, ExportStatusOut | ErrorResponse]:
        job_result = AsyncResult(job_id)

        response_data = {
            "job_id": job_id,
            "status": job_result.status,
        }

        if job_result.status == "SUCCESS":
            response_data["download_url"] = job_result.result

        elif job_result.status == "FAILURE":
            return HTTPStatus.BAD_REQUEST, ErrorResponse(error_code="export_status_error", detail=str(job_result.info))

        return HTTPStatus.OK, ExportStatusOut.from_orm(response_data)

    def get_all_categories(self, request) -> tuple[int, list[str] | ErrorResponse]:
        categories = self._dataset_service.get_all_categories()
        return HTTPStatus.OK, categories

    def create_category(self, request, category_data: CategorySchema) -> tuple[int, CategoryOut | ErrorResponse]:
        category = self._dataset_service.create_category(category_data)
        return HTTPStatus.CREATED, category

    def delete_category(self, request, category_data: CategorySchema) -> tuple[int, SuccessResponse | ErrorResponse]:
        self._dataset_service.delete_category(category_data)
        return HTTPStatus.OK, SuccessResponse(detail="Category delete successfully")


class TaskHandlers:
    def __init__(self, task_service: TaskService):
        self._task_service = task_service

    def get_all_tasks(self, request) -> tuple[int, list[TaskOut] | ErrorResponse]:
        tasks = self._task_service.get_all_tasks()
        return HTTPStatus.OK, tasks

    def get_task_by_id(self, request, task_id: int) -> tuple[int, TaskOut | ErrorResponse]:
        task = self._task_service.get_task_by_id(task_id)
        return HTTPStatus.OK, task

    def delete_task(self, request, task_id: int) -> tuple[int, SuccessResponse | ErrorResponse]:
        self._task_service.delete_task(task_id)
        return HTTPStatus.OK, SuccessResponse(detail="Task delete successfully")


class AssignmentHandlers:
    def __init__(self, assignment_service: AssignmentService):
        self._assignment_service = assignment_service

    def get_assignments_by_user(self, request, user_id: UUID) -> tuple[int, list[AssignmentHistoryOut] | ErrorResponse]:
        assignments = self._assignment_service.get_assignments_by_user(user_id)
        return HTTPStatus.OK, assignments

    def get_completed_assignments_by_user(
        self, request, user_id: UUID
    ) -> tuple[int, list[AssignmentHistoryOut] | ErrorResponse]:
        assignments = self._assignment_service.get_completed_assignments_by_user(user_id)
        return HTTPStatus.OK, assignments

    def create_assignment(
        self, request, user_id: UUID, pool_id: int
    ) -> tuple[int, AssignmentHistoryOut | AssignmentActiveOut | ErrorResponse]:
        assignment = self._assignment_service.create_assignment(user_id, pool_id)
        return HTTPStatus.CREATED, assignment

    def update_assignment(
        self, request, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema
    ) -> tuple[int, AssignmentActiveOut | ErrorResponse]:
        updated = self._assignment_service.update_assignment(user_id, assignment_id, annotation_data)
        return HTTPStatus.OK, updated


class AuthHandlers:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def create_tokens(self, request, data: LogIn) -> tuple[int, TokenOut | ErrorResponse]:
        token = self._auth_service.create_tokens(data)
        return HTTPStatus.OK, token

    def update_revoked_status(self, request, data: RefreshTokenIn) -> tuple[int, bool | ErrorResponse]:
        self._auth_service.update_revoked_status(data)
        return HTTPStatus.OK, SuccessResponse(detail="Logout successfully")

    def update_token(self, request, data: RefreshTokenIn) -> tuple[int, TokenOut | ErrorResponse]:
        token = self._auth_service.update_token(data)
        return HTTPStatus.OK, token

    def register_user(self, request, data: RegisterSchema) -> tuple[int, RegisterOut | ErrorResponse]:
        user = self._auth_service.register_user(data)
        return HTTPStatus.CREATED, user


class AnalyticsHandlers:
    def __init__(self, analytics_service: AnalyticsService):
        self._analytics_service = analytics_service

    def get_pools_progress(
        self, request, user_id: UUID, filters: PoolsProgressFilter
    ) -> tuple[int, list[PoolProgressOut] | ErrorResponse]:
        progress = self._analytics_service.get_pools_progress(user_id, filters)
        return HTTPStatus.OK, progress

    def get_users_info(self, request, filters: UserInfoFilter) -> tuple[int, list[UserInfoOut] | ErrorResponse]:
        info = self._analytics_service.get_users_info(filters)
        return HTTPStatus.OK, info
