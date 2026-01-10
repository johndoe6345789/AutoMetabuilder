"""Workflow plugin: create OpenAI client."""
import os
from openai import OpenAI

DEFAULT_ENDPOINT = "https://models.github.ai/inference"


def run(runtime, _inputs):
    """Initialize OpenAI client."""
    token = runtime.context.get("github_token")
    
    # Create OpenAI client
    client = OpenAI(
        base_url=os.environ.get("GITHUB_MODELS_ENDPOINT", DEFAULT_ENDPOINT),
        api_key=token,
    )
    
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["client"] = client
    return {"result": client, "initialized": client is not None}
