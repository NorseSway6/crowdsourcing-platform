from typing import Optional

from ninja import Schema
from pydantic import AliasPath, Field, PastDatetime, computed_field


class TaskSchema(Schema):
    dataset_id: int = Field(...)


class TaskOut(TaskSchema):
    task_id: int = Field(...)
    pool_id: Optional[int] = Field(...)
    image_url: str = Field()
    created_at: PastDatetime = Field(...)
