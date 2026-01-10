"""Workflow plugin: load and register plugins."""
from ....loaders.plugin_loader import load_plugins


def run(runtime, _inputs):
    """Load and register plugins."""
    tool_map = runtime.context.get("tool_map", {})
    tools = runtime.context.get("tools", [])
    load_plugins(tool_map, tools)
    return {"result": True}
