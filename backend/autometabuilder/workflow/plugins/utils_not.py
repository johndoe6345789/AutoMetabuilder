"""Workflow plugin: boolean not."""
from ..value_helpers import ValueHelpers


def run(_runtime, inputs):
    """Negate a boolean value."""
    return {"result": not ValueHelpers.coerce_bool(inputs.get("value"))}
