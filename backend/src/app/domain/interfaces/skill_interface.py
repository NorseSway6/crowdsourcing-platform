from typing import Any, List

from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema


class ISkillRepository:
    def get_all_skills(self) -> List[str]:
        pass

    def create_skill(self, skill_data: SkillSchema) -> SkillSchema:
        pass

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        pass

    def get_skills_by_names(self, names: List[str]) -> List[Skill]:
        pass
