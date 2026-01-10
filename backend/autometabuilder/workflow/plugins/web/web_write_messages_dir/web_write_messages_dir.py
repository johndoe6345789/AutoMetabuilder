"""Workflow plugin: write messages directory."""
from pathlib import Path
from ....data.messages_io import write_messages_dir


def run(_runtime, inputs):
    """Write messages to directory."""
    base_dir = inputs.get("base_dir")
    payload_content = inputs.get("payload_content", {})
    
    if not base_dir:
        return {"error": "base_dir is required"}
    
    write_messages_dir(Path(base_dir), payload_content)
    return {"result": "Messages written successfully"}
