from ninja import Schema
from pydantic import Field


class SkillSchema(Schema):
    name: str = Field(..., max_length=255)
