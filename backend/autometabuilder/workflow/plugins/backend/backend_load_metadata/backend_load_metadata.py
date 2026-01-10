"""Workflow plugin: load metadata."""
from .....utils import load_metadata as util_load_metadata


def run(runtime, _inputs):
    """Load metadata.json."""
    metadata = util_load_metadata()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["metadata"] = metadata
    return {"result": metadata}
