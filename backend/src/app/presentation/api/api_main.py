from ninja import NinjaAPI

from app.db.repositories.assignment_repository import AssignmentRepository
from app.db.repositories.dataset_repository import DatasetRepository
from app.db.repositories.platform_user_repository import UserRepository
from app.db.repositories.pool_repository import PoolRepository
from app.db.repositories.skill_repository import SkillRepository
from app.db.repositories.task_repository import TaskRepository
from app.domain.services.assignment_service import AssignmentService
from app.domain.services.dataset_service import DatasetService
from app.domain.services.platform_user_service import UserService
from app.domain.services.pool_service import PoolService
from app.domain.services.skill_service import SkillService
from app.domain.services.task_service import TaskService
from app.presentation.api.handlers import (
    AssignmentHandlers,
    DatasetHandlers,
    PoolHandlers,
    SkillHandlers,
    TaskHandlers,
    UserHandlers,
)
from app.presentation.routers.assignments_router import add_assignments_router
from app.presentation.routers.dataset_router import add_datasets_router
from app.presentation.routers.platforn_user_router import add_users_router
from app.presentation.routers.pool_router import add_pools_router
from app.presentation.routers.skill_router import add_skills_router
from app.presentation.routers.task_router import add_tasks_router


def get_api():
    api = NinjaAPI(
        title="Crowdsourcing Platform API",
        version="1.0.0",
    )

    # Skills build
    skill_repo = SkillRepository()
    skill_service = SkillService(skill_repo)
    skill_handlers = SkillHandlers(skill_service)
    add_skills_router(api, skill_handlers)

    # Users build
    user_repo = UserRepository()
    user_service = UserService(user_repo, skill_repo)
    user_handlers = UserHandlers(user_service)
    add_users_router(api, user_handlers)

    # Pools build
    pool_repo = PoolRepository()
    pool_service = PoolService(pool_repo, skill_repo)
    pool_handlers = PoolHandlers(pool_service)
    add_pools_router(api, pool_handlers)

    # Dataset build
    dataset_repo = DatasetRepository()
    dataset_service = DatasetService(dataset_repo)
    dataset_handlers = DatasetHandlers(dataset_service)
    add_datasets_router(api, dataset_handlers)

    # Tasks build
    task_repo = TaskRepository()
    task_service = TaskService(task_repo)
    task_handlers = TaskHandlers(task_service)
    add_tasks_router(api, task_handlers)

    # Assignment build
    assignment_repo = AssignmentRepository()
    assignment_service = AssignmentService(assignment_repo)
    assignment_handlers = AssignmentHandlers(assignment_service)
    add_assignments_router(api, assignment_handlers)

    return api


ninja_api = get_api()
