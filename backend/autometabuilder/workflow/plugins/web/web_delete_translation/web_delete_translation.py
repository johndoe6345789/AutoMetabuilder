"""Workflow plugin: delete translation."""
import json
import shutil
from pathlib import Path
from autometabuilder.utils import load_metadata


def run(_runtime, inputs):
    """Delete a translation."""
    lang = inputs.get("lang")
    if not lang:
        return {"error": "lang is required"}
    
    # Cannot delete English
    if lang == "en":
        return {"result": False}
    
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
    
    # Check if translation exists
    if lang not in messages_map:
        return {"result": False}
    
    # Delete the file/directory
    target = package_root / messages_map[lang]
    if target.exists():
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    
    # Update metadata
    del messages_map[lang]
    metadata_base["messages"] = messages_map
    (package_root / "metadata.json").write_text(
        json.dumps(metadata_base, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    return {"result": True}
