"""Workflow plugin: list translations."""
from ....data.translations import list_translations


def run(_runtime, _inputs):
    """List all available translations."""
    translations = list_translations()
    return {"result": translations}
