"""Load tool specs from JSON."""
import json
import os


def load_tools(metadata: dict) -> list:
    tools_path = os.path.join(os.path.dirname(__file__), metadata.get("tools_path", "tools.json"))
    with open(tools_path, "r", encoding="utf-8") as f:
        return json.load(f)
