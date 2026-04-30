from typing import Any, List

from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository


class SkillRepository(ISkillRepository):
    def get_all_skills(self) -> List[SkillSchema]:
        return Skill.objects.all()

    def set_skills(self, obj: Any, skills_data: dict) -> None:
        if not skills_data:
            obj.skills.clear()
            return

        names = [s.get("name") for s in skills_data]

        skills_qs = Skill.objects.filter(name__in=names)
        obj.skills.set(skills_qs)
