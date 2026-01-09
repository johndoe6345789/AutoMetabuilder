"""Load tool registry entries."""
import json
import os


def load_tool_registry() -> list:
    """Load tool registry entries."""
    path = os.path.join(os.path.dirname(__file__), "tool_registry.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []
