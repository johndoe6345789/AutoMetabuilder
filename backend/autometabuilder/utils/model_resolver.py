"""Resolve the LLM model name."""
import os

DEFAULT_MODEL = "openai/gpt-4o"


def resolve_model_name(prompt: dict) -> str:
    """Resolve model name from env or prompt."""
    return os.environ.get("LLM_MODEL", prompt.get("model", DEFAULT_MODEL))
