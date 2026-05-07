from typing import Any, List

from app.domain.entities.skill_schema import SkillSchema


class ISkillRepository:
    def get_all_skills(self) -> List[SkillSchema]:
        pass

    def set_skills(self, obj: Any, skills_data: dict) -> None:
        pass

    def create_skill(self, skill_data: SkillSchema) -> SkillSchema:
        pass

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        pass
