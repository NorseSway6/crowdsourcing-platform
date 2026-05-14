from ninja import Schema
from pydantic import Field


class ErrorResponse(Schema):
    detail: str = Field(...)


class SuccessResponse(Schema):
    detail: str = Field(...)
