import uuid
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import EmailStr, Field, PastDatetime

from app.domain.entities.user_profile_schema import ProfileSchema


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    VALIDATOR = "VALIDATOR"


class UserSchema(Schema):
    email: EmailStr = Field(...)
    role: UserRole = Field(...)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(default=True)
    profile: Optional[ProfileSchema] = Field(None, alias="user_profile")


class UserIn(UserSchema):
    user_id: uuid.UUID = Field(...)


class UserOut(UserSchema):
    user_id: uuid.UUID = Field(...)
