from typing import List

from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository


class SkillService:
    def __init__(self, skill_repo: ISkillRepository):
        self._skill_repo = skill_repo

    def get_all_skills(self) -> List[str]:
        return self._skill_repo.get_all_skills()

    def create_skill(self, skill_data: SkillSchema) -> SkillSchema:
        return self._skill_repo.create_skill(skill_data)

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        return self._skill_repo.delete_skill(skill_data)
