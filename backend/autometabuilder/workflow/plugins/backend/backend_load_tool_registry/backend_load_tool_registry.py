"""Workflow plugin: load tool registry."""
import json
import os
from pathlib import Path


def _load_tool_registry() -> list:
    """Load tool registry entries."""
    # Locate tool_registry.json relative to autometabuilder package root
    path = Path(__file__).resolve().parents[4] / "tool_registry.json"
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def run(runtime, _inputs):
    """Load tool registry entries."""
    tool_registry = _load_tool_registry()
    # Store in context for other plugins
    runtime.context["tool_registry"] = tool_registry
    return {"result": tool_registry}
