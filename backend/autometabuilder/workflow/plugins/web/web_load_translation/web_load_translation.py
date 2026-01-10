"""Workflow plugin: load translation."""
import json
from pathlib import Path
from autometabuilder.utils import load_metadata


def run(_runtime, inputs):
    """Load translation for a specific language."""
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
    
    # Resolve target path for language
    if lang in messages_map:
        target = messages_map[lang]
    elif (package_root / "messages" / lang).exists():
        target = f"messages/{lang}"
    else:
        target = f"messages_{lang}.json"
    
    if not target:
        return {"result": {}}
    
    translation = load_messages(package_root / target)
    return {"result": translation}
