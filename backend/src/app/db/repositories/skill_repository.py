from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_repository_interface import ISkillRepository


class SkillRepository(ISkillRepository):
    def get_all_skills(self) -> SkillSchema:
        return Skill.objects.all()
