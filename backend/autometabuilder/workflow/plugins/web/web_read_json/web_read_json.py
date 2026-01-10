"""Workflow plugin: read JSON file."""
from pathlib import Path
from ....data.json_utils import read_json


def run(_runtime, inputs):
    """Read JSON file."""
    path = inputs.get("path")
    if not path:
        return {"error": "path is required"}
    
    json_data = read_json(Path(path))
    return {"result": json_data}
