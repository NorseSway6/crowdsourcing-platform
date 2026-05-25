from typing import List, Optional
from uuid import UUID

from ninja import Schema
from pydantic import Field

from app.domain.entities.pool_schema import PoolSchema


class PipelineSchema(Schema):
    name: str = Field(...)
    dataset_id: int = Field(...)
    limit: Optional[int] = Field(default=None)
    pools: List[PoolSchema] = Field(default=[])


class PipelineOut(PipelineSchema):
    pipeline_id: int = Field(...)
    owner_id: UUID = Field(...)
