"""Workflow plugin: load tool policies."""
from ....loaders.tool_policy_loader import load_tool_policies


def run(runtime, _inputs):
    """Load tool_policies.json."""
    tool_policies = load_tool_policies()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["tool_policies"] = tool_policies
    return {"result": tool_policies}
