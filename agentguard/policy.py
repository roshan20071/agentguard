from typing import Any

from pydantic import BaseModel, Field

from .audit import AuditLogger
from .detectors import detect
from .models import Decision, Evaluation


class Policy(BaseModel):
    allowed_tools: set[str] = Field(default_factory=set)
    blocked_tools: set[str] = Field(default_factory=set)
    max_risk_score: float = Field(default=0.7, ge=0.0, le=1.0)
    deny_on_findings: bool = True


class AgentGuard:
    def __init__(self, policy: Policy | None = None, audit: AuditLogger | None = None) -> None:
        self.policy = policy or Policy()
        self.audit = audit or AuditLogger()

    def check_text(self, text: str, event_type: str = "text") -> Evaluation:
        findings = detect(text)
        score = max((finding.severity for finding in findings), default=0.0)
        reasons = [finding.detail for finding in findings]
        allowed = not (self.policy.deny_on_findings and findings) and score <= self.policy.max_risk_score
        result = Evaluation(allowed=allowed, decision=Decision.ALLOW if allowed else Decision.DENY,
                            reasons=reasons, risk_score=score)
        self.audit.record(event_type, allowed, reasons, risk_score=score)
        return result

    def check_input(self, text: str) -> Evaluation:
        return self.check_text(text, "input")

    def check_output(self, text: str) -> Evaluation:
        return self.check_text(text, "output")

    def check_tool(self, tool: str, arguments: dict[str, Any] | None = None) -> Evaluation:
        reasons: list[str] = []
        if tool in self.policy.blocked_tools:
            reasons.append(f"Tool '{tool}' is explicitly blocked")
        elif self.policy.allowed_tools and tool not in self.policy.allowed_tools:
            reasons.append(f"Tool '{tool}' is not allowlisted")
        result = Evaluation(allowed=not reasons, decision=Decision.ALLOW if not reasons else Decision.DENY,
                            reasons=reasons, risk_score=1.0 if reasons else 0.0,
                            metadata={"tool": tool, "arguments_present": bool(arguments)})
        self.audit.record("tool", result.allowed, reasons, tool=tool)
        return result
