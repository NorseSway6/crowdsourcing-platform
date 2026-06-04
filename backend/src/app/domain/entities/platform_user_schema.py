import uuid
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import EmailStr, Field, PastDatetime

from app.domain.entities.auth_schema import TokenOut
from app.domain.entities.user_profile_schema import ProfileSchema


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


class UserSchema(Schema):
    email: EmailStr = Field(...)
    role: UserRole = Field(...)
    user_profile: Optional[ProfileSchema] = Field(None)


class UserOut(UserSchema):
    user_id: uuid.UUID = Field(...)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(default=True)


class RegisterSchema(UserSchema):
    password: str = Field(..., min_length=8, max_length=64)


class RegisterOut(Schema):
    user: UserOut = Field(...)
    tokens: TokenOut = Field(...)
