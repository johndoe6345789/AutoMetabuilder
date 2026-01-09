"""Workflow plugin: load SDLC context."""
from ...context_loader import get_sdlc_context


def run(runtime, inputs):
    return {"context": get_sdlc_context(runtime.context["gh"], runtime.context["msgs"])}
