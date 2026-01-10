"""Workflow plugin: get recent logs."""
from ....data.logs import get_recent_logs


def run(_runtime, inputs):
    """Get recent log entries."""
    lines = inputs.get("lines", 50)
    logs = get_recent_logs(lines)
    return {"result": logs}
