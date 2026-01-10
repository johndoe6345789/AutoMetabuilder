"""Load metadata.json."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

METADATA_PATH = Path(__file__).resolve().parent / "metadata.json"
INCLUDED_SECTIONS = {
    "settings_descriptions_path": "settings_descriptions",
    "suggestions_path": "suggestions",
    "workflow_plugins_path": "workflow_plugins",
}


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata() -> dict[str, Any]:
    """Load metadata.json with optional section includes."""
    metadata = _read_json(METADATA_PATH)
    base_dir = METADATA_PATH.parent
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
