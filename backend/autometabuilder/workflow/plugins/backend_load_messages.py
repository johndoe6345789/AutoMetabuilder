"""Workflow plugin: load translation messages."""
from ... import load_messages


def run(_runtime, _inputs):
    """Load translation messages."""
    messages = load_messages()
    return {"result": messages}
