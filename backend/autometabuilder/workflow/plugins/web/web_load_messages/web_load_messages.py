"""Workflow plugin: load messages."""
import json
from pathlib import Path


def run(_runtime, inputs):
    """Load translation messages from path."""
    path = inputs.get("path")
    if not path:
        return {"error": "path is required"}
    
    path_obj = Path(path)
    
    # Helper function to read JSON
    def read_json(p):
        if not p.exists():
            return {}
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    
    # If directory, merge all JSON files
    if path_obj.is_dir():
        merged = {}
        for file_path in sorted(path_obj.glob("*.json")):
            merged.update(read_json(file_path))
        return {"result": merged}
    
    # If file, just read it
    return {"result": read_json(path_obj)}
