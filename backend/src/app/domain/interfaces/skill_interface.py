from typing import List

from app.domain.entities.skill_schema import SkillSchema


class ISkillRepository:
    def get_all_skills(self) -> List[SkillSchema]:
        pass
