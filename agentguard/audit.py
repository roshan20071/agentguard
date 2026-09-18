from datetime import datetime, timezone
from typing import Any, Protocol
from uuid import uuid4

from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    allowed: bool
    reasons: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuditSink(Protocol):
    def write(self, event: AuditEvent) -> None: ...


class AuditLogger:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def write(self, event: AuditEvent) -> None:
        self.events.append(event)

    def record(self, event_type: str, allowed: bool, reasons: list[str], **metadata: Any) -> AuditEvent:
        event = AuditEvent(event_type=event_type, allowed=allowed, reasons=reasons, metadata=metadata)
        self.write(event)
        return event
