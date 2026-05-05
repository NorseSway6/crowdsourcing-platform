import uuid
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import Field, FutureDatetime, PastDatetime


class AssignmentStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AssignmentSchema(Schema):
    annotation: dict = Field(default={})


class AssignmentOut(AssignmentSchema):
    task_id: int = Field(...)
    user_id: uuid.UUID = Field(...)
    assignment_id: int = Field(...)
    started_at: PastDatetime = Field(...)
    status: AssignmentStatus = Field(...)
    completed_at: Optional[PastDatetime] = Field(...)
