"""
AutoMetabuilder package.
"""
import os
import json


def load_messages():
    """Load messages based on APP_LANG environment variable."""
    lang = os.environ.get("APP_LANG", "en")
    messages_path = os.path.join(
        os.path.dirname(__file__), f"messages_{lang}.json"
    )
    if not os.path.exists(messages_path):
        # Fallback to English if the requested language file doesn't exist
        messages_path = os.path.join(
            os.path.dirname(__file__), "messages_en.json"
        )
    with open(messages_path, "r", encoding="utf-8") as f:
        return json.load(f)
