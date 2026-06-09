from ninja import NinjaAPI

from app.db.repositories.assignment_repository import AssignmentRepository
from app.db.repositories.auth_repository import AuthRepository
from app.db.repositories.dataset_repository import DatasetRepository
from app.db.repositories.pipeline_repository import PipelineRepository
from app.db.repositories.platform_user_repository import UserRepository
from app.db.repositories.pool_repository import PoolRepository
from app.db.repositories.skill_repository import SkillRepository
from app.db.repositories.task_repository import TaskRepository
from app.domain.exceptions import DomainException
from app.domain.services.assignment_service import AssignmentService
from app.domain.services.auth_service import AuthService
from app.domain.services.consensus_service import ConsensusService
from app.domain.services.dataset_service import DatasetService
from app.domain.services.export_service import ExportService
from app.domain.services.pipeline_engine import PipelineEngine
from app.domain.services.platform_user_service import UserService
from app.domain.services.pool_service import PoolService
from app.domain.services.skill_service import SkillService
from app.domain.services.task_service import TaskService
from app.presentation.api.auth import JWTAuth
from app.presentation.api.handlers import (
    AssignmentHandlers,
    AuthHandlers,
    DatasetHandlers,
    PipelineHandlers,
    PoolHandlers,
    SkillHandlers,
    TaskHandlers,
    UserHandlers,
)
from app.presentation.routers.assignments_router import add_assignments_router
from app.presentation.routers.auth_router import add_auth_router
from app.presentation.routers.dataset_router import add_datasets_router
from app.presentation.routers.pipeline_router import add_pipelines_router
from app.presentation.routers.platforn_user_router import add_users_router
from app.presentation.routers.pool_router import add_pools_router
from app.presentation.routers.skill_router import add_skills_router
from app.presentation.routers.task_router import add_tasks_router


def get_api():
    api = NinjaAPI(
        title="Crowdsourcing Platform API",
        version="1.0.0",
        auth=JWTAuth(),
    )

    # Build repositories
    skill_repo = SkillRepository()
    user_repo = UserRepository()
    pool_repo = PoolRepository()
    dataset_repo = DatasetRepository()
    task_repo = TaskRepository()
    assignment_repo = AssignmentRepository()
    pipeline_repo = PipelineRepository()
    auth_repo = AuthRepository()

    # Build services
    consensus_service = ConsensusService(assignment_repo, pool_repo, task_repo)
    task_service = TaskService(task_repo, pool_repo)
    skill_service = SkillService(skill_repo)
    user_service = UserService(user_repo, skill_repo)
    pool_service = PoolService(pool_repo, skill_repo, task_repo)
    dataset_service = DatasetService(dataset_repo)
    pipeline_engine = PipelineEngine(
        task_repo, assignment_repo, consensus_service, pool_repo, pipeline_repo, skill_repo, task_service, pool_service
    )
    assignment_service = AssignmentService(assignment_repo, task_repo, pipeline_engine, pool_repo)
    export_service = ExportService(task_repo, dataset_repo)
    auth_service = AuthService(auth_repo, user_repo, user_service)

    # Build handlers
    skill_handlers = SkillHandlers(skill_service)
    user_handlers = UserHandlers(user_service)
    pool_handlers = PoolHandlers(pool_service)
    dataset_handlers = DatasetHandlers(dataset_service, export_service)
    task_handlers = TaskHandlers(task_service)
    assignment_handlers = AssignmentHandlers(assignment_service)
    pipeline_handlers = PipelineHandlers(pipeline_engine)
    auth_handlers = AuthHandlers(auth_service)

    # Endpoints registration
    add_skills_router(api, skill_handlers)
    add_users_router(api, user_handlers)
    add_pools_router(api, pool_handlers)
    add_datasets_router(api, dataset_handlers)
    add_tasks_router(api, task_handlers)
    add_assignments_router(api, assignment_handlers)
    add_pipelines_router(api, pipeline_handlers)
    add_auth_router(api, auth_handlers)

    return api


ninja_api = get_api()


@ninja_api.exception_handler(DomainException)
def domain_exception_handler(request, exc: DomainException):
    return ninja_api.create_response(
        request, {"detail": exc.message, "error_code": exc.error_code}, status=exc.status_code
    )
