from app.domain.interfaces.skill_repository_interface import ISkillRepository


class SkillService:
    def __init__(self, skill_repo: ISkillRepository):
        self._skill_repo = skill_repo

    def get_all_skills(self):
        return self._skill_repo.get_all_skills()
