from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema


class ISkillRepository:
    def get_all_skills(self) -> list[str]:
        pass

    def create_skill(self, skill_data: SkillSchema) -> Skill:
        pass

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        pass

    def get_skills_by_names(self, names: list[str]) -> list[Skill]:
        pass
