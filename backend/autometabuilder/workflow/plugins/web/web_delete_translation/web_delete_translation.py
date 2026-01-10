"""Workflow plugin: delete translation."""
from ....data.translations import delete_translation


def run(_runtime, inputs):
    """Delete a translation."""
    lang = inputs.get("lang")
    if not lang:
        return {"error": "lang is required"}
    
    deleted = delete_translation(lang)
    return {"result": deleted}
