"""Workflow plugin: handle /api/workflow/plugins endpoint."""


def run(_runtime, _inputs):
    """Return workflow plugins metadata."""
    from autometabuilder.utils import load_metadata
    metadata = load_metadata()
    plugins = metadata.get("workflow_plugins", {})
    return {"result": {"plugins": plugins}}
