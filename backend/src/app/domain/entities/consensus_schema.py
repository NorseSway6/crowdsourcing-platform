from typing import Any, Optional

from ninja import Schema
from pydantic import Field


class ConsensusSchema(Schema):
    is_consensus_reached: bool = Field(...)
    final_annotation: Optional[Any] = Field(default=None)
    verdict: Optional[str] = Field(default=None)
