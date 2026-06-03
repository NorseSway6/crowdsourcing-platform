from ninja import Schema
from pydantic import Field


class ErrorResponse(Schema):
    detail: str = Field(...)
    error_code: str = Field(...)


class SuccessResponse(Schema):
    detail: str = Field(...)
