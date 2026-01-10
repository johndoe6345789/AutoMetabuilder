"""Workflow plugin: build tool map."""
import importlib
import json
import os
from pathlib import Path


def _load_callable(path: str):
    """Import and return a callable."""
    module_path, attr = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)


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


def _build_tool_map(gh, registry_entries: list) -> dict:
    """Build tool name to callable map."""
    tool_map = {}
    for entry in registry_entries:
        name = entry.get("name")
        provider = entry.get("provider")
        if not name:
            continue
        if provider == "github":
            method = entry.get("method")
            tool_map[name] = getattr(gh, method) if gh and method else None
            continue
        if provider == "module":
            path = entry.get("callable")
            tool_map[name] = _load_callable(path) if path else None
            continue
        tool_map[name] = None
    return tool_map


def run(runtime, _inputs):
    """Build tool registry map."""
    gh = runtime.context.get("gh")
    registry = _load_tool_registry()
    tool_map = _build_tool_map(gh, registry)
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["tool_map"] = tool_map
    return {"result": tool_map}
