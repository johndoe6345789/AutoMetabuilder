"""Workflow plugin: load prompt configuration."""
from ....loaders.prompt_loader import load_prompt_yaml
from ....utils.model_resolver import resolve_model_name


def run(runtime, _inputs):
    """Load prompt.yml."""
    prompt = load_prompt_yaml()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["prompt"] = prompt
    # Update model_name based on loaded prompt
    runtime.context["model_name"] = resolve_model_name(prompt)
    return {"result": prompt}
