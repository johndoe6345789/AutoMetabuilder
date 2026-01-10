"""Workflow plugin: handle /api/translation-options endpoint."""


def run(_runtime, _inputs):
    """Return available translations."""
    from autometabuilder.data import list_translations
    translations = list_translations()
    return {"result": {"translations": translations}}
