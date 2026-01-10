"""
AutoMetabuilder package.
"""
import os
import json


def load_messages():
    """Load messages based on APP_LANG environment variable and metadata."""
    metadata_path = os.path.join(os.path.dirname(__file__), "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            messages_map = metadata.get("messages", {})
    else:
        messages_map = {}

    lang = os.environ.get("APP_LANG", "en")
    
    # Get filename from metadata or fallback to default pattern
    messages_file = messages_map.get(lang, f"messages_{lang}.json")
    messages_path = os.path.join(os.path.dirname(__file__), messages_file)

    if not os.path.exists(messages_path):
        # Fallback to English from metadata or default messages_en.json
        en_file = messages_map.get("en", "messages_en.json")
        messages_path = os.path.join(os.path.dirname(__file__), en_file)
    
    with open(messages_path, "r", encoding="utf-8") as f:
        return json.load(f)
