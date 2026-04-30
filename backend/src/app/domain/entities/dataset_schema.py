from ninja import Schema
from pydantic import Field, PastDatetime


class DatasetSchema(Schema):
    name: str = Field(..., max_length=255)
    domain: str = Field(..., max_length=255)
    owner: int = Field(...)
    created_at: PastDatetime = Field(...)


class DatasetOut(DatasetSchema):
    dataset_id: int = Field(...)
