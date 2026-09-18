from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class Evaluation(BaseModel):
    allowed: bool
    decision: Decision
    reasons: list[str] = Field(default_factory=list)
    risk_score: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class InputRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    session_id: str | None = None


class OutputRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    session_id: str | None = None


class ToolRequest(BaseModel):
    tool: str = Field(min_length=1, max_length=200)
    arguments: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None
