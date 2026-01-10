"""Workflow plugin: delete variable from store."""


def run(runtime, inputs):
    """Delete variable from workflow store."""
    key = inputs.get("key")
    
    if key and key in runtime.store:
        del runtime.store[key]
        return {"result": True, "deleted": True}
    
    return {"result": False, "deleted": False}
