import uuid
from typing import Optional

from ninja import Schema
from pydantic import EmailStr, Field, PastDatetime

from app.domain.entities.user_profile_schema import ProfileSchema


class UserSchema(Schema):
    email: EmailStr = Field(...)
    role: str = Field(..., max_length=10)
    created_at: PastDatetime = Field(...)
    is_active: bool = Field(..., default=True)
    profile: Optional[ProfileSchema] = Field(None)


class UserIn(UserSchema):
    user_id: uuid.UUID = Field(...)


class UserOut(UserSchema):
    user_id: uuid.UUID = Field(...)
