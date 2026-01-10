"""Workflow plugin: create GitHub integration."""
from ....github_service import create_github_integration


def run(runtime, _inputs):
    """Initialize GitHub client."""
    token = runtime.context.get("github_token")
    msgs = runtime.context.get("msgs", {})
    
    gh = create_github_integration(token, msgs)
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["gh"] = gh
    return {"result": gh, "initialized": gh is not None}
