"""Workflow plugin: build context for API."""
import os
from ....web.routes.context import build_context


def run(_runtime, _inputs):
    """
    Build the complete context object for the web UI.
    
    This includes logs, env vars, translations, metadata, navigation,
    prompt, workflow, packages, messages, and status.
    
    Returns:
        dict: Complete context object
    """
    context = build_context()
    return {"result": context}
