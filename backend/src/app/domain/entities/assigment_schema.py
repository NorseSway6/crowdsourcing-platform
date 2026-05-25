import uuid
from enum import Enum
from typing import List, Literal, Optional, Union

from ninja import Schema
from pydantic import Field, PastDatetime, RootModel


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


class CocoAnnotation(Schema):
    type: Literal["coco"] = "coco"
    items: List[AssignmentCocoItem] = Field(default=[])


class VerificationAnnotation(Schema):
    type: Literal["verification"] = "verification"
    is_correct: bool = Field(...)


class ClassificationAnnotation(Schema):
    type: Literal["classification"] = "classification"
    category_id: int = Field(...)


class AssignmentSchema(Schema):
    annotation: Optional[Union[CocoAnnotation, VerificationAnnotation, ClassificationAnnotation]] = Field(
        default=None, discriminator="type"
    )


class AssignmentOut(AssignmentSchema):
    task_id: int = Field(...)
    user_id: uuid.UUID = Field(...)
    assignment_id: int = Field(...)
    pool_id: int = Field(...)
    started_at: PastDatetime = Field(...)
    status: AssignmentStatus = Field(...)
    completed_at: Optional[PastDatetime] = Field(...)

    @staticmethod
    def resolve_pool_id(obj):
        return obj.task.pool_id
