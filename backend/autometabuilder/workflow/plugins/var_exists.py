"""Workflow plugin: check if variable exists."""


def run(runtime, inputs):
    """Check if variable exists in workflow store."""
    key = inputs.get("key")
    return {"result": key in runtime.store if key else False}
