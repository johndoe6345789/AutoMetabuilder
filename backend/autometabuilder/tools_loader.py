"""Load tool specs from JSON."""
import json
import os


def load_tools(metadata: dict) -> list:
    """Load tool specs from metadata reference."""
    tools_path = os.path.join(os.path.dirname(__file__), metadata.get("tools_path", "tools.json"))
    if os.path.isdir(tools_path):
        tools = []
        for filename in sorted(os.listdir(tools_path)):
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(tools_path, filename), "r", encoding="utf-8") as f:
                tools.extend(json.load(f))
        return tools
    with open(tools_path, "r", encoding="utf-8") as f:
        return json.load(f)
