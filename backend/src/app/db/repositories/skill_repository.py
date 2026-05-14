from typing import Any, List

from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository


class SkillRepository(ISkillRepository):
    def get_all_skills(self) -> List[str]:
        skills = Skill.objects.all()
        if not skills:
            raise HttpError(404, "Skill not found")
        return [s.name for s in skills]

    def set_skills(self, obj: Any, skills_data: dict) -> None:  # убрать
        if not skills_data:
            obj.skills.clear()
            return

        names = [s.get("name") for s in skills_data]

        skills_qs = Skill.objects.filter(name__in=names)
        obj.skills.set(skills_qs)

    def create_skill(self, skill_data: SkillSchema) -> SkillSchema:
        try:
            skill = Skill.objects.create(name=skill_data.name)
        except IntegrityError:
            raise HttpError(409, "Update failed due to integrity error")
        return SkillSchema.from_orm(skill)

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        deleted, _ = Skill.objects.filter(name=skill_data.name).delete()
        if not deleted:
            raise HttpError(404, "Skill for delete not found")
        return deleted
