from django.core.cache import cache
from django.db import IntegrityError

from app.db.models.skill import Skill
from app.domain.entities.skill_schema import SkillSchema
from app.domain.interfaces.skill_interface import ISkillRepository
from config import settings


class SkillRepository(ISkillRepository):
    CACHE_KEY = "all_skills_list"

    def get_all_skills(self) -> list[Skill]:
        cached_skills = cache.get(self.CACHE_KEY)
        if cached_skills:
            return cached_skills

        skills = list(Skill.objects.all())

        cache.set(self.CACHE_KEY, skills, settings.CACHE_TIMEOUT)

        return skills

    def create_skill(self, skill_data: SkillSchema) -> Skill:
        try:
            skill, created = Skill.objects.get_or_create(name=skill_data.name)

            if created:
                cache.delete(self.CACHE_KEY)
        except IntegrityError:
            return None

        return skill

    def delete_skill(self, skill_data: SkillSchema) -> bool:
        deleted, _ = Skill.objects.filter(name=skill_data.name).delete()

        if deleted > 0:
            cache.delete(self.CACHE_KEY)

        return deleted > 0

    def get_skills_by_names(self, names: list[str]) -> list[Skill]:
        return list(Skill.objects.filter(name__in=names))
