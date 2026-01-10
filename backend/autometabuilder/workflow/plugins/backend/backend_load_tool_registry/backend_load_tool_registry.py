"""Workflow plugin: load tool registry."""
from ....loaders.tool_registry_loader import load_tool_registry


def run(runtime, _inputs):
    """Load tool registry entries."""
    tool_registry = load_tool_registry()
    # Store in context for other plugins
    runtime.context["tool_registry"] = tool_registry
    return {"result": tool_registry}
