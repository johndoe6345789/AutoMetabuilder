"""Workflow plugin: load translation messages."""
from ... import load_messages


def run(runtime, _inputs):
    """Load translation messages."""
    messages = load_messages()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["msgs"] = messages
    return {"result": messages}
