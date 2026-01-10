"""Load prompt configuration."""
import os
import yaml

DEFAULT_PROMPT_PATH = "prompt.yml"


def load_prompt_yaml() -> dict:
    """Load prompt YAML from disk."""
    local_path = os.environ.get("PROMPT_PATH", DEFAULT_PROMPT_PATH)
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    raise FileNotFoundError(f"Prompt file not found at {local_path}")
