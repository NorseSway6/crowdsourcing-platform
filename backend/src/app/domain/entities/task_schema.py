from ninja import Schema
from pydantic import Field, HttpUrl, PastDatetime


class TaskSchema(Schema):
    pool: int = Field(...)
    dataset: int = Field(...)
    image_url: HttpUrl = Field(...)
    created_at: PastDatetime = Field(...)


class TaskIn(TaskSchema):
    task_id: int = Field(...)


class TaskOut(TaskSchema):
    task_id: int = Field(...)
