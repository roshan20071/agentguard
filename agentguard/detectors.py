import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    name: str
    severity: float
    detail: str


PATTERNS: tuple[tuple[str, str, float], ...] = (
    ("prompt_override", r"\b(ignore|disregard|override)\s+(all|any|previous|prior)\s+instructions\b", 0.9),
    ("system_prompt_extraction", r"\b(reveal|show|print|give)\b.{0,40}\b(system prompt|hidden instructions)\b", 0.8),
    ("credential_exfiltration", r"\b(api[_ -]?key|secret|password|access token)\b.{0,30}\b(send|post|upload|share|reveal)\b", 0.95),
)


def detect(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for name, pattern, severity in PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            findings.append(Finding(name, severity, f"Detected {name.replace('_', ' ')} pattern"))
    return findings
