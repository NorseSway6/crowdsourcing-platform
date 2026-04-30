from ninja import NinjaAPI

from app.db.repositories.platform_user_repository import UserRepository
from app.db.repositories.pool_repository import PoolRepository
from app.db.repositories.profile_repository import ProfileRepository
from app.db.repositories.skill_repository import SkillRepository
from app.domain.services.platform_user_service import UserService
from app.domain.services.pool_service import PoolService
from app.domain.services.skill_service import SkillService
from app.presentation.api.handlers import PoolHandlers, SkillHandlers, UserHandlers
from app.presentation.routers.platforn_user_router import add_users_router
from app.presentation.routers.pool_router import add_pools_router
from app.presentation.routers.skill_router import add_skills_router


def get_api():
    api = NinjaAPI(
        title="Crowdsourcing Platform API",
        version="1.0.0",
    )

    # Users build
    user_repo = UserRepository()
    profile_repo = ProfileRepository()
    user_service = UserService(user_repo, profile_repo)
    user_handlers = UserHandlers(user_service)
    add_users_router(api, user_handlers)

    # Pools build
    pool_repo = PoolRepository()
    pool_service = PoolService(pool_repo)
    pool_handlers = PoolHandlers(pool_service)
    add_pools_router(api, pool_handlers)

    # Skills build
    skill_repo = SkillRepository()
    skill_service = SkillService(skill_repo)
    skill_handlers = SkillHandlers(skill_service)
    add_skills_router(api, skill_handlers)

    return api


ninja_api = get_api()
