"""Workflow plugin: list translations."""
import json
from pathlib import Path
from autometabuilder.loaders.metadata_loader import load_metadata


def run(_runtime, _inputs):
    """List all available translations."""
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    
    # Get messages map from metadata
    metadata = load_metadata()
    metadata_base = json.loads((package_root / "metadata.json").read_text(encoding="utf-8"))
    messages_map = metadata_base.get("messages", {})
    
    if messages_map:
        return {"result": messages_map}
    
    # Fallback: scan for messages files
    fallback = {}
    for candidate in package_root.glob("messages_*.json"):
        name = candidate.name
        language = name.removeprefix("messages_").removesuffix(".json")
        fallback[language] = name
    
    messages_dir = package_root / "messages"
    if messages_dir.exists():
        for candidate in messages_dir.iterdir():
            if candidate.is_dir():
                fallback[candidate.name] = f"messages/{candidate.name}"
    
    return {"result": fallback}
