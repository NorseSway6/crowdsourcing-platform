from ninja import Schema
from pydantic import Field, HttpUrl, PastDatetime


class TaskSchema(Schema):
    dataset_id: int = Field(...)
    image_url: HttpUrl = Field(...)


class TaskOut(TaskSchema):
    task_id: int = Field(...)
    pool_id: int = Field(...)
    created_at: PastDatetime = Field(...)
