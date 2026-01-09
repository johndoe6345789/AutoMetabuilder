"""Workflow plugin: filter list."""
import re
from ..value_helpers import ValueHelpers


def run(runtime, inputs):
    items = ValueHelpers.ensure_list(inputs.get("items"))
    mode = inputs.get("mode", "contains")
    pattern = inputs.get("pattern", "")
    filtered = []
    for item in items:
        candidate = str(item)
        matched = False
        if mode == "contains":
            matched = pattern in candidate
        elif mode == "regex":
            matched = bool(re.search(pattern, candidate))
        elif mode == "equals":
            matched = candidate == pattern
        elif mode == "not_equals":
            matched = candidate != pattern
        elif mode == "starts_with":
            matched = candidate.startswith(pattern)
        elif mode == "ends_with":
            matched = candidate.endswith(pattern)
        if matched:
            filtered.append(item)
    return {"items": filtered}
