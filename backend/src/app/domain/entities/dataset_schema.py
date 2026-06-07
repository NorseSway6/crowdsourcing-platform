import uuid

from ninja import Schema
from pydantic import Field, PastDatetime


class CategorySchema(Schema):
    name: str


class CategoryOut(CategorySchema):
    id: int


class DatasetSchema(Schema):
    name: str = Field(..., max_length=255)
    domain: str = Field(..., max_length=255)
    categories: list[str] = Field(...)


class DatasetOut(DatasetSchema):
    dataset_id: int = Field(...)
    owner_id: uuid.UUID = Field(...)
    created_at: PastDatetime = Field(...)

    categories: list[CategoryOut] = Field(...)
