"""Workflow plugin: load translation."""
from ....data.translations import load_translation


def run(_runtime, inputs):
    """Load translation for a specific language."""
    lang = inputs.get("lang", "en")
    translation = load_translation(lang)
    return {"result": translation}
