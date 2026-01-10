"""Workflow plugin: branch condition."""
import re
from ...value_helpers import ValueHelpers


def run(_runtime, inputs):
    """Evaluate a branch condition."""
    value = inputs.get("value")
    mode = inputs.get("mode", "is_truthy")
    compare = inputs.get("compare", "")
    decision = False

    if mode == "is_empty":
        decision = not ValueHelpers.ensure_list(value)
    elif mode == "is_truthy":
        decision = bool(value)
    elif mode == "equals":
        decision = str(value) == compare
    elif mode == "not_equals":
        decision = str(value) != compare
    elif mode == "contains":
        decision = compare in str(value)
    elif mode == "regex":
        decision = bool(re.search(compare, str(value)))

    return {"result": decision}
