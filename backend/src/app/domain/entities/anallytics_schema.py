from typing import Any, List, Optional

from ninja import Schema
from pydantic import Field


class PoolProgressOut(Schema):
    pool_id: int = Field(...)
    pool_type: str = Field(...)
    total_tasks: int = Field(...)
    completed_tasks: int = Field(...)
    progress_percentage: float = Field(...)


class PoolsProgressFilter(Schema):
    pipline_id: Optional[int] = Field(None)
    pool_type: Optional[str] = Field(None)


class UserInfoOut(Schema):
    last_name: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=30)
    middle_name: Optional[str] = Field(None, max_length=30)
    group: Optional[str] = Field(None, max_length=15)
    institution: Optional[str] = Field(None, max_length=100)
    submitted: int = Field(...)
    approved: int = Field(...)
    user_accuracy: int = Field(...)


class UserInfoFilter(Schema):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    institution: Optional[str] = Field(None)
    group: Optional[str] = Field(None)
