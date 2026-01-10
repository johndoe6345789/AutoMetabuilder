"""Workflow plugin: set variable in store."""


def run(runtime, inputs):
    """Set variable in workflow store."""
    key = inputs.get("key")
    value = inputs.get("value")
    
    if key:
        runtime.store[key] = value
        return {"result": value, "key": key}
    
    return {"result": None, "error": "No key provided"}
