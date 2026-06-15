from enum import Enum
from typing import Any, List, Optional

from ninja import Schema
from pydantic import ConfigDict, Field, PastDatetime, PositiveInt, field_validator


class PoolType(str, Enum):
    ANNOTATION = "ANNOTATION"
    VERIFICATION = "VERIFICATION"


class PoolStatus(str, Enum):
    OPEN = "OPEN"
    COMPLETED = "COMPLETED"


class PoolInstructionSchema(Schema):
    title: str = Field(...)
    content_markdown: str = Field(...)


class PoolInstructionOut(PoolInstructionSchema):
    id: int = Field(...)


class PoolSchema(Schema):
    points: int = Field(...)
    skills: Optional[List[str]] = Field(default=[])
    pool_type: PoolType = Field(...)
    target_institution: Optional[str] = Field(None)
    tasks_limit: int = Field(...)
    time_limit: int = Field(...)
    instruction_id: Optional[int] = Field(None)


class PoolOut(PoolSchema):
    overlap: PositiveInt = Field(...)
    pool_id: int = Field(...)
    pipeline_id: int = Field(...)
    order: int = Field(...)
    created_at: PastDatetime = Field(...)
    status: PoolStatus = Field(...)
    skills: List[Any] = Field(default=[])

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_validator("skills", mode="before")
    @classmethod
    def transform_skills_to_names(cls, v: Any) -> List[str]:
        if hasattr(v, "all"):
            v = v.all()

        if isinstance(v, (list, tuple)) or hasattr(v, "__iter__"):
            return [skill.name if hasattr(skill, "name") else str(skill) for skill in v]

        return v


class PoolDetailOut(PoolOut):
    instruction: Optional[PoolInstructionOut] = Field(None)


class PoolFilter(Schema):
    skills: Optional[List[str]] = Field(None)
    min_points: Optional[int] = Field(None)
    max_points: Optional[int] = Field(None)
    institution: Optional[str] = Field(None)
