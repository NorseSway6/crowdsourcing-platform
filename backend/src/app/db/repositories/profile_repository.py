from typing import List
from uuid import UUID

from app.db.models.skill import Skill
from app.db.models.user_profile import UserProfile
from app.domain.entities.platform_user_schema import UserIn, UserOut
from app.domain.entities.skill_schema import SkillSchema
from app.domain.entities.user_profile_schema import ProfileSchema
from app.domain.interfaces.user_profile_interface import IProfileRepository


class ProfileRepository(IProfileRepository):
    def set_profile(self, user: UserIn, profile_data: dict) -> ProfileSchema:
        profile, _ = UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        return profile

    def set_skills(self, profile: ProfileSchema, skills_data: List[SkillSchema]) -> None:
        if not skills_data:
            profile.skills.clear()
        else:
            names = [s.get("name") for s in skills_data]
            skills_qs = Skill.objects.filter(name__in=names)
            profile.skills.set(skills_qs)

    def update_profile(self, user_id: UUID, profile_data: ProfileSchema) -> ProfileSchema:
        profile, _ = UserProfile.objects.update_or_create(user__user_id=user_id, defaults=profile_data)
        return profile
