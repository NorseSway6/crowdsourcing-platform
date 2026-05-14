from typing import List, Optional

from ninja import Schema
from pydantic import Field


class ProfileSchema(Schema):
    last_name: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=30)
    middle_name: Optional[str] = Field(None, max_length=30)
    group: Optional[str] = Field(None, max_length=15)
    institution: Optional[str] = Field(None, max_length=100)
    skills: Optional[List[str]] = Field(default=[])

    @staticmethod
    def resolve_skills(obj):
        if isinstance(obj, dict):
            return obj.get("skills", [])

        if hasattr(obj, "skills"):
            return [skill.name for skill in obj.skills.all()]
