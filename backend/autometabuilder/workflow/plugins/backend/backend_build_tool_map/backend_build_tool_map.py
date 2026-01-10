"""Workflow plugin: build tool map."""
from ....loaders.callable_loader import load_callable
from ....loaders.tool_registry_loader import load_tool_registry


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
            tool_map[name] = load_callable(path) if path else None
            continue
        tool_map[name] = None
    return tool_map


def run(runtime, _inputs):
    """Build tool registry map."""
    gh = runtime.context.get("gh")
    registry = load_tool_registry()
    tool_map = _build_tool_map(gh, registry)
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["tool_map"] = tool_map
    return {"result": tool_map}
