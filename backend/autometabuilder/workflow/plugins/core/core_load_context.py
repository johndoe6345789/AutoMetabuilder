"""Workflow plugin: load SDLC context."""
from ....utils.context_loader import get_sdlc_context


def run(runtime, _inputs):
    """Load SDLC context into the workflow store."""
    return {"context": get_sdlc_context(runtime.context["gh"], runtime.context["msgs"])}
