"""Workflow plugin: write messages directory."""
import json
from pathlib import Path


def run(_runtime, inputs):
    """Write messages to directory."""
    base_dir = inputs.get("base_dir")
    payload_content = inputs.get("payload_content", {})
    
    if not base_dir:
        return {"error": "base_dir is required"}
    
    base_dir_path = Path(base_dir)
    base_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Group messages by prefix
    grouped = {}
    for key, value in payload_content.items():
        parts = key.split(".")
        group = ".".join(parts[:2]) if len(parts) >= 2 else "root"
        grouped.setdefault(group, {})[key] = value
    
    # Remove old files not in desired set
    existing = {path.stem for path in base_dir_path.glob("*.json")}
    desired = set(grouped.keys())
    for name in existing - desired:
        (base_dir_path / f"{name}.json").unlink()
    
    # Write grouped files
    for name, entries in grouped.items():
        target_path = base_dir_path / f"{name}.json"
        target_path.write_text(
            json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )
    
    return {"result": "Messages written successfully"}
