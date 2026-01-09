"""Workflow plugin: boolean not."""
from ..value_helpers import ValueHelpers


def run(runtime, inputs):
    return {"result": not ValueHelpers.coerce_bool(inputs.get("value"))}
