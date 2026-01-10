"""Workflow plugin: load metadata."""
import json
from pathlib import Path
from typing import Any


INCLUDED_SECTIONS = {
    "settings_descriptions_path": "settings_descriptions",
    "suggestions_path": "suggestions",
    "workflow_plugins_path": "workflow_plugins",
}


def _read_json(path: Path) -> dict[str, Any]:
    """Read JSON file."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_metadata() -> dict[str, Any]:
    """Load metadata.json with optional section includes."""
    # Locate metadata.json relative to the autometabuilder package root
    metadata_path = Path(__file__).resolve().parents[4] / "metadata.json"
    metadata = _read_json(metadata_path)
    base_dir = metadata_path.parent
    for path_key, dest_key in INCLUDED_SECTIONS.items():
        include_path = metadata.get(path_key)
        if include_path:
            resolved_path = base_dir / include_path
            if resolved_path.is_dir():
                merged: dict[str, Any] = {}
                for file_path in sorted(resolved_path.glob("*.json")):
                    merged.update(_read_json(file_path))
                metadata[dest_key] = merged
            else:
                metadata[dest_key] = _read_json(resolved_path)
    return metadata


def run(runtime, _inputs):
    """Load metadata.json."""
    metadata = _load_metadata()
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["metadata"] = metadata
    return {"result": metadata}
