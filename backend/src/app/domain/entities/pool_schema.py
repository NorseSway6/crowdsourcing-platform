from typing import List, Optional

from ninja import Schema
from pydantic import Field, PastDatetime, PositiveInt


class PoolSchema(Schema):
    points: int = Field(...)
    skills: Optional[List[str]] = Field(default=[])
    overlap: PositiveInt = Field(...)


class PoolIn(PoolSchema):
    dataset_id: int = Field(...)
    limit: Optional[int] = Field(...)


class PoolOut(PoolSchema):
    pool_id: int = Field(...)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(default=True)

    @staticmethod
    def resolve_skills(obj):
        return [s.name for s in obj.skills.all()]
