"""Workflow plugin: get variable from store."""


def run(runtime, inputs):
    """Get variable from workflow store."""
    key = inputs.get("key")
    default = inputs.get("default")
    
    value = runtime.store.get(key, default)
    return {"result": value, "exists": key in runtime.store}
