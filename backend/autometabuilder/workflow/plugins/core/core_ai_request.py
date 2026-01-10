"""Workflow plugin: AI request."""
from ....openai_client import get_completion


def run(runtime, inputs):
    """Invoke the model with current messages."""
    messages = list(inputs.get("messages") or [])
    response = get_completion(
        runtime.context["client"],
        runtime.context["model_name"],
        messages,
        runtime.context["tools"]
    )
    resp_msg = response.choices[0].message
    runtime.logger.info(
        resp_msg.content
        if resp_msg.content
        else runtime.context["msgs"]["info_tool_call_requested"]
    )
    messages.append(resp_msg)
    tool_calls = getattr(resp_msg, "tool_calls", None) or []
    return {
        "response": resp_msg,
        "has_tool_calls": bool(tool_calls),
        "tool_calls_count": len(tool_calls)
    }
