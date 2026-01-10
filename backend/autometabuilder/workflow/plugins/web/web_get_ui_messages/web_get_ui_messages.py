"""Workflow plugin: get UI messages."""
import json
from pathlib import Path
from autometabuilder.loaders.metadata_loader import load_metadata


def run(_runtime, inputs):
    """
    Get UI messages for a specific language with fallback to English.
    
    Inputs:
        lang: Language code (default: en)
        
    Returns:
        dict: UI messages with __lang key indicating the language
    """
    lang = inputs.get("lang", "en")
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    
    # Helper to read JSON
    def read_json(path_obj):
        if not path_obj.exists():
            return {}
        try:
            return json.loads(path_obj.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    
    # Helper to load messages from path
    def load_messages(path_obj):
        if path_obj.is_dir():
            merged = {}
            for file_path in sorted(path_obj.glob("*.json")):
                merged.update(read_json(file_path))
            return merged
        return read_json(path_obj)
    
    # Get messages map
    metadata = load_metadata()
    metadata_base = read_json(package_root / "metadata.json")
    messages_map = metadata_base.get("messages", {})
    
    # Resolve target path
    def resolve_target(language):
        if language in messages_map:
            return messages_map[language]
        if (package_root / "messages" / language).exists():
            return f"messages/{language}"
        return f"messages_{language}.json"
    
    # Load base (English) and localized messages
    base_name = resolve_target("en")
    base = load_messages(package_root / base_name)
    
    localized = load_messages(package_root / resolve_target(lang))
    
    # Merge with localized overriding base
    merged = dict(base)
    merged.update(localized)
    merged["__lang"] = lang
    
    return {"result": merged}
