"""Workflow plugin: update translation."""
from ....web.data.translations import update_translation


def run(_runtime, inputs):
    """Update an existing translation."""
    lang = inputs.get("lang")
    payload = inputs.get("payload", {})
    
    if not lang:
        return {"error": "lang is required"}
    
    updated = update_translation(lang, payload)
    return {"result": updated}
