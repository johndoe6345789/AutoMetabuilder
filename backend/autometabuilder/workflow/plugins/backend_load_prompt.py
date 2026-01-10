"""Workflow plugin: load prompt configuration."""
from ...prompt_loader import load_prompt_yaml


def run(_runtime, _inputs):
    """Load prompt.yml."""
    prompt = load_prompt_yaml()
    return {"result": prompt}
