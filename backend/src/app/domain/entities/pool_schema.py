from enum import Enum
from typing import Any, List, Optional

from ninja import Schema
from pydantic import ConfigDict, Field, PastDatetime, PositiveInt, field_validator


class PoolType(str, Enum):
    ANNOTATION = "ANNOTATION"
    VERIFICATION = "VERIFICATION"
    CLASSIFICATION = "CLASSIFICATION"


class PoolStatus(str, Enum):
    OPEN = "OPEN"
    COMPLETED = "COMPLETED"


class PoolSchema(Schema):
    points: int = Field(...)
    skills: Optional[List[str]] = Field(default=[])
    overlap: PositiveInt = Field(...)
    pool_type: PoolType = Field(...)


class PoolOut(PoolSchema):
    pool_id: int = Field(...)
    pipeline_id: int = Field(...)
    order: int = Field(...)
    created_at: PastDatetime = Field(...)
    status: PoolStatus = Field(...)

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
