from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import Field, PastDatetime


class TaskStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    COMPLETED = "COMPLETED"


class TaskSchema(Schema):
    dataset_id: int = Field(...)


class TaskOut(TaskSchema):
    task_id: int = Field(...)
    pool_id: Optional[int] = Field(...)
    image_url: str = Field()
    created_at: PastDatetime = Field(...)
    status: TaskStatus = Field(...)
