from typing import Optional

from ninja import Schema
from pydantic import Field, FutureDatetime, PastDatetime


class AssigmentSchema(Schema):
    task: int = Field(...)
    user: int = Field(...)
    annotation: dict = Field(..., default={})
    status: str = Field(..., max_length=20)
    started_at: PastDatetime = Field(...)
    completed_at: Optional[FutureDatetime] = Field(...)
    status: str = Field(..., max_length=20)


class AssigmentIn(AssigmentSchema):
    assignment_id: int = Field(...)


class AssigmentOut(AssigmentSchema):
    assignment_id: int = Field(...)
