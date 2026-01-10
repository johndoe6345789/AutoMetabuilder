"""Workflow plugin: load tool policies."""
import json
import os
from pathlib import Path


def _load_tool_policies() -> dict:
    """Load tool policies JSON."""
    # Locate tool_policies.json relative to autometabuilder package root
    path = Path(__file__).resolve().parents[4] / "tool_policies.json"
    if not os.path.exists(path):
        return {"modifying_tools": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {"modifying_tools": []}
    return data if isinstance(data, dict) else {"modifying_tools": []}


def run(runtime, _inputs):
    """Load tool_policies.json."""
    tool_policies = _load_tool_policies()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["tool_policies"] = tool_policies
    return {"result": tool_policies}
