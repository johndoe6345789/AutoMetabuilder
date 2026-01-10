"""Workflow plugin: load messages."""
from pathlib import Path
from ....web.data.messages_io import load_messages


def run(_runtime, inputs):
    """Load translation messages from path."""
    path = inputs.get("path")
    if not path:
        return {"error": "path is required"}
    
    messages = load_messages(Path(path))
    return {"result": messages}
