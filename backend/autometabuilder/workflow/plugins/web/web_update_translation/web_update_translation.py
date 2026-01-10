"""Workflow plugin: update translation."""
import json
from pathlib import Path
from autometabuilder.utils import load_metadata


def run(_runtime, inputs):
    """Update an existing translation."""
    lang = inputs.get("lang")
    payload = inputs.get("payload", {})
    
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
    
    # Check if translation exists
    if lang not in messages_map:
        return {"result": False}
    
    payload_content = payload.get("content", {})
    target_path = package_root / messages_map[lang]
    
    # Write based on whether it's a directory or file
    if target_path.is_dir():
        # Group messages by prefix for directory structure
        target_path.mkdir(parents=True, exist_ok=True)
        
        grouped = {}
        for key, value in payload_content.items():
            parts = key.split(".")
            group = ".".join(parts[:2]) if len(parts) >= 2 else "root"
            grouped.setdefault(group, {})[key] = value
        
        # Remove old files not in desired set
        existing = {path.stem for path in target_path.glob("*.json")}
        desired = set(grouped.keys())
        for name in existing - desired:
            (target_path / f"{name}.json").unlink()
        
        # Write grouped files
        for name, entries in grouped.items():
            file_path = target_path / f"{name}.json"
            file_path.write_text(
                json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8"
            )
    else:
        # Write as single file
        target_path.write_text(
            json.dumps(payload_content, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )
    
    return {"result": True}
