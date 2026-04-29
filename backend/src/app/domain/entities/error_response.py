from ninja import Schema
from pydantic import Field


class ErrorResponse(Schema):
    message: str = Field(...)
