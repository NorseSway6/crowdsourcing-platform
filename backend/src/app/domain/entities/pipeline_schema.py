from typing import List, Optional
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict, Field

from app.domain.entities.pool_schema import PoolOut, PoolSchema


class PipelineSchema(Schema):
    name: str = Field(...)
    dataset_id: int = Field(...)
    limit: Optional[int] = Field(default=None)


class PipelineIn(PipelineSchema):
    pools: List[PoolSchema] = Field(default=[])


class PipelineOut(PipelineSchema):
    pipeline_id: int = Field(...)
    owner_id: UUID = Field(...)
    pools: List[PoolOut] = Field(..., validation_alias="pool_pipeline", serialization_alias="pools")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
