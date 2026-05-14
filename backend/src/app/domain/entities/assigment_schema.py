import uuid
from enum import Enum
from typing import List, Optional

from ninja import Schema
from pydantic import Field, PastDatetime


class AssignmentStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AssignmentCocoItem(Schema):
    category_id: int = Field(...)
    bbox: List[float] = Field(...)
    segmentation: List[List[float]] = Field(default=[])
    area: float = Field(...)
    iscrowd: int = Field(...)


class AssignmentSchema(Schema):
    annotation: List[AssignmentCocoItem] = Field(default=[])


class AssignmentOut(AssignmentSchema):
    task_id: int = Field(...)
    user_id: uuid.UUID = Field(...)
    assignment_id: int = Field(...)
    started_at: PastDatetime = Field(...)
    status: AssignmentStatus = Field(...)
    completed_at: Optional[PastDatetime] = Field(...)
