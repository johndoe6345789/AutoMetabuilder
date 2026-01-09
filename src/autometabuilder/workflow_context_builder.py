"""Build workflow runtime context."""
from .model_resolver import resolve_model_name


def build_workflow_context(parts: dict) -> dict:
    """Build the workflow context dict."""
    prompt = parts["prompt"]
    context = dict(parts)
    context["model_name"] = resolve_model_name(prompt)
    return context
