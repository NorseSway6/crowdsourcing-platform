from typing import List

from ninja import Schema
from pydantic import Field, PastDatetime, PositiveInt

from app.domain.entities.skill_schema import SkillSchema


class PoolSchema(Schema):
    points: int = Field(...)
    skills: List[SkillSchema] = Field(...)
    overlap: PositiveInt = Field(...)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(...)


class PoolOut(PoolSchema):
    pool_id: int = Field(...)
