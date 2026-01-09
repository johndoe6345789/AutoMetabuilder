"""Load tool policies from JSON."""
import json
import os


def load_tool_policies() -> dict:
    """Load tool policies JSON."""
    path = os.path.join(os.path.dirname(__file__), "tool_policies.json")
    if not os.path.exists(path):
        return {"modifying_tools": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {"modifying_tools": []}
    return data if isinstance(data, dict) else {"modifying_tools": []}
