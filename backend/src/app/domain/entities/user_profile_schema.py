from typing import List, Optional

from ninja import Schema
from pydantic import Field

from app.domain.entities.skill_schema import SkillSchema


class ProfileSchema(Schema):
    last_name: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=30)
    middle_name: Optional[str] = Field(None, max_length=30)
    group_number: Optional[str] = Field(None, max_length=15)
    institution: Optional[str] = Field(None, max_length=100)
    skills: Optional[List[SkillSchema]] = Field(None, default=[])
