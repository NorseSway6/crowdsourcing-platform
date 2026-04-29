from app.domain.entities.skill_schema import SkillSchema


class ISkillRepository:
    def get_all_skills(self) -> SkillSchema:
        pass
