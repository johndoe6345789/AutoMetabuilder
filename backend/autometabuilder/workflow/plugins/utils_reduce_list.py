"""Workflow plugin: reduce list."""
from ..value_helpers import ValueHelpers


def run(_runtime, inputs):
    """Reduce a list into a string."""
    items = ValueHelpers.ensure_list(inputs.get("items"))
    separator = ValueHelpers.normalize_separator(inputs.get("separator", ""))
    reduced = separator.join([str(item) for item in items])
    return {"result": reduced}
