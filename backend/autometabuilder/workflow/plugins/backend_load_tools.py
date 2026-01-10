"""Workflow plugin: load tools."""
from ...tools_loader import load_tools


def run(runtime, _inputs):
    """Load tool definitions."""
    metadata = runtime.context.get("metadata", {})
    tools = load_tools(metadata)
    return {"result": tools}
