from fastapi import FastAPI

from .models import InputRequest, OutputRequest, ToolRequest
from .policy import AgentGuard, Policy

app = FastAPI(title="AgentGuard", version="0.1.0")
guard = AgentGuard(Policy())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/check/input")
def check_input(request: InputRequest):
    return guard.check_input(request.text)


@app.post("/v1/check/output")
def check_output(request: OutputRequest):
    return guard.check_output(request.text)


@app.post("/v1/check/tool")
def check_tool(request: ToolRequest):
    return guard.check_tool(request.tool, request.arguments)


@app.get("/v1/audit")
def audit_events():
    return guard.audit.events
