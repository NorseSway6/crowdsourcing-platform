import uuid

from ninja import Schema
from pydantic import Field, PastDatetime


class DatasetSchema(Schema):
    name: str = Field(..., max_length=255)
    domain: str = Field(..., max_length=255)


class DatasetOut(DatasetSchema):
    dataset_id: int = Field(...)
    owner_id: uuid.UUID = Field(...)
    created_at: PastDatetime = Field(...)
