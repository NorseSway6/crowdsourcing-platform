from typing import List

from ninja import NinjaAPI, Router

from app.domain.entities.error_response import ErrorResponse
from app.domain.entities.skill_schema import SkillSchema
from app.presentation.api.handlers import SkillHandlers


def get_skills_router(skill_handlers: SkillHandlers):
    router = Router(tags=["skills"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: skill_handlers.get_all_skills(request),
        response={200: List[SkillSchema], 404: ErrorResponse},
    )

    return router


def add_skills_router(api: NinjaAPI, skill_handlers: SkillHandlers):
    skills_router = get_skills_router(skill_handlers)
    api.add_router("/skills", skills_router)
