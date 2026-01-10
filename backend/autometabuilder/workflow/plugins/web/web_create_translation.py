"""Workflow plugin: create translation."""
from ....web.data.translations import create_translation


def run(_runtime, inputs):
    """Create a new translation."""
    lang = inputs.get("lang")
    if not lang:
        return {"error": "lang is required"}
    
    created = create_translation(lang)
    return {"result": created}
