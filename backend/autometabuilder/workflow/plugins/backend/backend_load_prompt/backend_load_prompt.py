"""Workflow plugin: load prompt configuration."""
import os
import yaml

DEFAULT_PROMPT_PATH = "prompt.yml"
DEFAULT_MODEL = "openai/gpt-4o"


def _load_prompt_yaml() -> dict:
    """Load prompt YAML from disk."""
    local_path = os.environ.get("PROMPT_PATH", DEFAULT_PROMPT_PATH)
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    raise FileNotFoundError(f"Prompt file not found at {local_path}")


def _resolve_model_name(prompt: dict) -> str:
    """Resolve model name from env or prompt."""
    return os.environ.get("LLM_MODEL", prompt.get("model", DEFAULT_MODEL))


def run(runtime, _inputs):
    """Load prompt.yml."""
    prompt = _load_prompt_yaml()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["prompt"] = prompt
    # Update model_name based on loaded prompt
    runtime.context["model_name"] = _resolve_model_name(prompt)
    return {"result": prompt}
