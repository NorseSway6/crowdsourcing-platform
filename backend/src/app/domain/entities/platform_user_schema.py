import uuid
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import ConfigDict, EmailStr, Field, PastDatetime

from app.domain.entities.user_profile_schema import ProfileSchema


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    VALIDATOR = "VALIDATOR"


class UserSchema(Schema):
    email: EmailStr = Field(...)
    role: UserRole = Field(...)
    profile: Optional[ProfileSchema] = Field(None, alias="user_profile")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserOut(UserSchema):
    user_id: uuid.UUID = Field(...)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(default=True)
