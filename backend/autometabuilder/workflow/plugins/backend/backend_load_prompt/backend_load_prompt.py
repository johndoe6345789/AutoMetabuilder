"""Workflow plugin: load prompt configuration."""
import os
from ....loaders.prompt_loader import load_prompt_yaml

DEFAULT_MODEL = "openai/gpt-4o"


def _resolve_model_name(prompt: dict) -> str:
    """Resolve model name from env or prompt."""
    return os.environ.get("LLM_MODEL", prompt.get("model", DEFAULT_MODEL))


def run(runtime, _inputs):
    """Load prompt.yml."""
    prompt = load_prompt_yaml()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["prompt"] = prompt
    # Update model_name based on loaded prompt
    runtime.context["model_name"] = _resolve_model_name(prompt)
    return {"result": prompt}
