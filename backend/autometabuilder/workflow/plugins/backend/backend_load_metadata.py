"""Workflow plugin: load metadata."""
from ....loaders.metadata_loader import load_metadata


def run(runtime, _inputs):
    """Load metadata.json."""
    metadata = load_metadata()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["metadata"] = metadata
    return {"result": metadata}
