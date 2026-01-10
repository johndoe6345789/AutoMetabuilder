"""Utility functions for AutoMetabuilder.

This module provides helper functions that are used across the codebase.
These are pure utility functions that don't contain business logic.
"""
import json
import os
import yaml
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    """Read JSON file."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata() -> dict[str, Any]:
    """Load metadata.json with optional section includes.
    
    This is a utility function for loading metadata configuration.
    """
    included_sections = {
        "settings_descriptions_path": "settings_descriptions",
        "suggestions_path": "suggestions",
        "workflow_plugins_path": "workflow_plugins",
    }
    
    # Locate metadata.json relative to the autometabuilder package root
    metadata_path = Path(__file__).resolve().parent / "metadata.json"
    metadata = read_json(metadata_path)
    base_dir = metadata_path.parent
    
    for path_key, dest_key in included_sections.items():
        include_path = metadata.get(path_key)
        if include_path:
            resolved_path = base_dir / include_path
            if resolved_path.is_dir():
                merged: dict[str, Any] = {}
                for file_path in sorted(resolved_path.glob("*.json")):
                    merged.update(read_json(file_path))
                metadata[dest_key] = merged
            else:
                metadata[dest_key] = read_json(resolved_path)
    
    return metadata


def load_prompt_yaml() -> dict:
    """Load prompt YAML from disk.
    
    This is a utility function for loading prompt configuration.
    """
    default_prompt_path = "prompt.yml"
    local_path = os.environ.get("PROMPT_PATH", default_prompt_path)
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    raise FileNotFoundError(f"Prompt file not found at {local_path}")
