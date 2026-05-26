from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository


class SkillService:
    def __init__(self, skill_repo: ISkillRepository):
        self._skill_repo = skill_repo

    def get_all_skills(self) -> list[str]:
        skills = self._skill_repo.get_all_skills()
        if not skills:
            return None
        return [s.name for s in skills]

    def create_skill(self, skill_data: SkillSchema) -> SkillSchema:
        skill = self._skill_repo.create_skill(skill_data)
        if not skill:
            return None
        return SkillSchema.from_orm(skill)

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        deleted = self._skill_repo.delete_skill(skill_data)
        if not deleted:
            return None
        return deleted
