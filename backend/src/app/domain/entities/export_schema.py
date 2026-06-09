from typing import Any, Dict, Optional

from ninja import Schema
from pydantic import Field


class CompletedTaskData(Schema):
    task_id: int = Field(...)
    image_path: str = Field(...)
    shapes: list[Dict[str, Any]] = Field(...)
    width: int = Field(...)
    height: int = Field(...)


class ExportStatusOut(Schema):
    job_id: str = Field(...)
    status: str = Field(...)
    download_url: Optional[str] = Field(None)
