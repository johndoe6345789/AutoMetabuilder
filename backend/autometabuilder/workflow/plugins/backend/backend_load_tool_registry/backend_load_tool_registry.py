"""Workflow plugin: load tool registry."""
from .....utils import load_tool_registry as util_load_tool_registry


def run(runtime, _inputs):
    """Load tool registry entries."""
    tool_registry = util_load_tool_registry()
    # Store in context for other plugins
    runtime.context["tool_registry"] = tool_registry
    return {"result": tool_registry}
