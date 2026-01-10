"""Workflow plugin: load tools."""
from ...tools_loader import load_tools


def run(runtime, _inputs):
    """Load tool definitions."""
    metadata = runtime.context.get("metadata", {})
    tools = load_tools(metadata)
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["tools"] = tools
    return {"result": tools}
