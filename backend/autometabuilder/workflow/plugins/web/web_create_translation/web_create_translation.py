"""Workflow plugin: create translation."""
import json
import shutil
from pathlib import Path
from autometabuilder.utils import load_metadata


def run(_runtime, inputs):
    """Create a new translation."""
    lang = inputs.get("lang")
    if not lang:
        return {"error": "lang is required"}
    
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    
    # Helper to read JSON
    def read_json(path_obj):
        if not path_obj.exists():
            return {}
        try:
            return json.loads(path_obj.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    
    # Load metadata
    metadata_base = read_json(package_root / "metadata.json")
    messages_map = metadata_base.get("messages", {})
    
    # Check if translation already exists
    if lang in messages_map:
        return {"result": False}
    
    # Resolve base target
    def resolve_target(language):
        if language in messages_map:
            return messages_map[language]
        if (package_root / "messages" / language).exists():
            return f"messages/{language}"
        return f"messages_{language}.json"
    
    base = resolve_target("en")
    base_file = package_root / base
    
    if not base_file.exists():
        return {"result": False}
    
    # Copy base to new language
    if base_file.is_dir():
        target_name = f"messages/{lang}"
        target_path = package_root / target_name
        shutil.copytree(base_file, target_path)
    else:
        target_name = f"messages_{lang}.json"
        target_path = package_root / target_name
        shutil.copy(base_file, target_path)
    
    # Update metadata
    messages_map[lang] = target_name
    metadata_base["messages"] = messages_map
    (package_root / "metadata.json").write_text(
        json.dumps(metadata_base, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    return {"result": True}
