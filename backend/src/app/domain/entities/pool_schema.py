from enum import Enum
from typing import List, Optional

from ninja import Schema
from pydantic import Field, PastDatetime, PositiveInt


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

    @staticmethod
    def resolve_skills(obj):
        return [s.name for s in obj.skills.all()]
