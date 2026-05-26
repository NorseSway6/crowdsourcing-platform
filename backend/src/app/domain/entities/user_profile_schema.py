from typing import Any, List, Optional

from ninja import Schema
from pydantic import ConfigDict, Field, field_validator


class ProfileSchema(Schema):
    last_name: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=30)
    middle_name: Optional[str] = Field(None, max_length=30)
    group: Optional[str] = Field(None, max_length=15)
    institution: Optional[str] = Field(None, max_length=100)

    skills: List[Any] = Field(default=[])

    model_config = ConfigDict(from_attributes=True)

    @field_validator("skills", mode="before")
    @classmethod
    def transform_skills_to_names(cls, v: Any) -> List[str]:
        if hasattr(v, "all"):
            v = v.all()

        if isinstance(v, (list, tuple)) or hasattr(v, "__iter__"):
            return [skill.name if hasattr(skill, "name") else str(skill) for skill in v]

        return v
