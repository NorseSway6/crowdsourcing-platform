from typing import List

from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository


class SkillService:
    def __init__(self, skill_repo: ISkillRepository):
        self._skill_repo = skill_repo

    def get_all_skills(self) -> List[SkillSchema]:
        return self._skill_repo.get_all_skills()
