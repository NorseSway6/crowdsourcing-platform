from django.db import IntegrityError

from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository


class SkillRepository(ISkillRepository):
    def get_all_skills(self) -> list[Skill]:
        return list(Skill.objects.all())

    def create_skill(self, skill_data: SkillSchema) -> Skill:
        try:
            skill = Skill.objects.create(name=skill_data.name)
        except IntegrityError:
            return None

        return skill

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        deleted, _ = Skill.objects.filter(name=skill_data.name).delete()
        return deleted > 0

    def get_skills_by_names(self, names: list[str]) -> list[Skill]:
        return list(Skill.objects.filter(name__in=names))
