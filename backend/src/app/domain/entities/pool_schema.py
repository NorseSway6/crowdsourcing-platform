from typing import List

from ninja import Schema
from pydantic import Field, PastDatetime, PositiveInt

from app.domain.entities.skill_schema import SkillSchema


class PoolSchema(Schema):
    points: PositiveInt = Field(..., default=0)
    skills: List[SkillSchema] = Field(..., default=[])
    overlap: PositiveInt = Field(..., default=1)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(..., default=True)


class PoolIn(PoolSchema):
    pool_id: int = Field(...)


class PoolOut(PoolSchema):
    pool_id: int = Field(...)
