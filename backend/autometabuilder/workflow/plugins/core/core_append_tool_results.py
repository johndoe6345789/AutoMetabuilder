"""Workflow plugin: append tool results."""
from ....integrations.notifications import notify_all
from ....utils.roadmap_utils import is_mvp_reached


def run(runtime, inputs):
    """Append tool results to the message list."""
    messages = list(inputs.get("messages") or [])
    tool_results = inputs.get("tool_results") or []
    if tool_results:
        messages.extend(tool_results)

    if runtime.context["args"].yolo and is_mvp_reached():
        runtime.logger.info("MVP reached. Stopping YOLO loop.")
        notify_all("AutoMetabuilder YOLO loop stopped: MVP reached.")

    return {"messages": messages}
