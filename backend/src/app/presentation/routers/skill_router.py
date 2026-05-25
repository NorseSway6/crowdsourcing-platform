from typing import List

from ninja import NinjaAPI, Router

from app.domain.entities.response_schema import ErrorResponse, SuccessResponse
from app.domain.entities.skill_schema import SkillSchema
from app.presentation.api.handlers import SkillHandlers


def get_skills_router(skill_handlers: SkillHandlers):
    router = Router(tags=["skills"])

    router.add_api_operation(
        "/",
        ["GET"],
        lambda request: skill_handlers.get_all_skills(request),
        response={200: List[str], 404: ErrorResponse},
    )

    def create_skill(request, data: SkillSchema) -> SkillSchema:
        return skill_handlers.create_skill(request, data)

    router.add_api_operation(
        "/",
        ["POST"],
        create_skill,
        response={201: SkillSchema, 400: ErrorResponse},
    )

    def delete_skill(request, data: SkillSchema) -> bool:
        return skill_handlers.delete_skill(request, data)

    router.add_api_operation(
        "/",
        ["DELETE"],
        delete_skill,
        response={200: SuccessResponse, 400: ErrorResponse},
    )

    return router


def add_skills_router(api: NinjaAPI, skill_handlers: SkillHandlers):
    skills_router = get_skills_router(skill_handlers)
    api.add_router("/skills", skills_router)
