"""Workflow plugin: run tool calls."""
from ...integrations.notifications import notify_all
from ..tool_calls_handler import handle_tool_calls


def run(runtime, inputs):
    resp_msg = inputs.get("response")
    tool_calls = getattr(resp_msg, "tool_calls", None) or []
    if not resp_msg:
        return {"tool_results": [], "no_tool_calls": True}

    tool_results = handle_tool_calls(
        resp_msg,
        runtime.context["tool_map"],
        runtime.context["msgs"],
        runtime.context["args"],
        runtime.context["tool_policies"],
        runtime.logger
    )
    if not tool_calls and resp_msg.content:
        notify_all(f"AutoMetabuilder task complete: {resp_msg.content[:100]}...")
    return {
        "tool_results": tool_results,
        "no_tool_calls": not bool(tool_calls)
    }
