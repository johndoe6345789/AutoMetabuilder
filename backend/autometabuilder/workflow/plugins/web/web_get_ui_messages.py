"""Workflow plugin: get UI messages."""
from ....web.data.translations import get_ui_messages


def run(_runtime, inputs):
    """
    Get UI messages for a specific language with fallback to English.
    
    Inputs:
        lang: Language code (default: en)
        
    Returns:
        dict: UI messages with __lang key indicating the language
    """
    lang = inputs.get("lang", "en")
    messages = get_ui_messages(lang)
    return {"result": messages}
