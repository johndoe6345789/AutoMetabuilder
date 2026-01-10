"""Workflow plugin: create OpenAI client."""
from ....openai_factory import create_openai_client


def run(runtime, _inputs):
    """Initialize OpenAI client."""
    token = runtime.context.get("github_token")
    
    client = create_openai_client(token)
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["client"] = client
    return {"result": client, "initialized": client is not None}
