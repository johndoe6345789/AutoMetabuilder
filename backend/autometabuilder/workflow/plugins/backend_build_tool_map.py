"""Workflow plugin: build tool map."""
from ...tool_map_builder import build_tool_map
from ...tool_registry_loader import load_tool_registry


def run(runtime, _inputs):
    """Build tool registry map."""
    gh = runtime.context.get("gh")
    registry = load_tool_registry()
    tool_map = build_tool_map(gh, registry)
    return {"result": tool_map}
