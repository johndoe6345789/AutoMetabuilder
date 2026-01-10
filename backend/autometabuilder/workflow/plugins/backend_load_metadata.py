"""Workflow plugin: load metadata."""
from ...metadata_loader import load_metadata


def run(_runtime, _inputs):
    """Load metadata.json."""
    metadata = load_metadata()
    return {"result": metadata}
