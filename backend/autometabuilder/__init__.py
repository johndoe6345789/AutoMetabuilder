"""
AutoMetabuilder package.
"""
import json
import os
from pathlib import Path

from .utils import load_metadata


def _load_messages_path(path: Path) -> dict:
    if path.is_dir():
        merged: dict = {}
        for file_path in sorted(path.glob("*.json")):
            with open(file_path, "r", encoding="utf-8") as f:
                merged.update(json.load(f))
        return merged
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _resolve_messages_path(lang: str, messages_map: dict, base_dir: Path) -> Path:
    candidates = []
    if lang in messages_map:
        candidates.append(base_dir / messages_map[lang])
    candidates.append(base_dir / "messages" / lang)
    candidates.append(base_dir / f"messages_{lang}.json")
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def load_messages():
    """Load messages based on APP_LANG environment variable and metadata."""
    metadata = load_metadata()
    messages_map = metadata.get("messages", {})

    lang = os.environ.get("APP_LANG", "en")

    base_dir = Path(__file__).resolve().parent
    messages_path = _resolve_messages_path(lang, messages_map, base_dir)
    if not messages_path.exists():
        messages_path = _resolve_messages_path("en", messages_map, base_dir)
    return _load_messages_path(messages_path)
