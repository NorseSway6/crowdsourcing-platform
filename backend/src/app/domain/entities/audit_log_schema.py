from ninja import Schema
from pydantic import Field, PastDatetime
from pydantic.networks import IPvAnyAddress


class AuditLogSchema(Schema):
    user: int = Field(...)
    task: int = Field(...)
    pool: int = Field(...)
    action: str = Field(..., max_length=255)
    details: dict = Field(default={})
    timestamp: PastDatetime = Field(...)
    ip_address: IPvAnyAddress = Field(...)


class AuditLogIn(AuditLogSchema):
    audit_id: int = Field(...)


class AuditLogOut(AuditLogSchema):
    audit_id: int = Field(...)
