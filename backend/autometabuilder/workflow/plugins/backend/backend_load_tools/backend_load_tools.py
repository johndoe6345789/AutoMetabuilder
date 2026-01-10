"""Workflow plugin: load tools."""
import json
import os
from pathlib import Path


def _load_tools(metadata: dict) -> list:
    """Load tool specs from metadata reference."""
    # Locate tools relative to autometabuilder package root
    base_dir = Path(__file__).resolve().parents[4]
    tools_path = base_dir / metadata.get("tools_path", "tools.json")
    
    if tools_path.is_dir():
        tools = []
        for filename in sorted(os.listdir(tools_path)):
            if not filename.endswith(".json"):
                continue
            with open(tools_path / filename, "r", encoding="utf-8") as f:
                tools.extend(json.load(f))
        return tools
    
    with open(tools_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run(runtime, _inputs):
    """Load tool definitions."""
    metadata = runtime.context.get("metadata", {})
    tools = _load_tools(metadata)
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["tools"] = tools
    return {"result": tools}
