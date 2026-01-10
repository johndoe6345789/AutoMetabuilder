from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .json_utils import read_json
from .paths import PACKAGE_ROOT


def load_messages(path: Path) -> dict[str, Any]:
    if path.is_dir():
        merged: dict[str, Any] = {}
        for file_path in sorted(path.glob("*.json")):
            merged.update(read_json(file_path))
        return merged
    return read_json(path)


def group_messages(payload_content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for key, value in payload_content.items():
        parts = key.split(".")
        group = ".".join(parts[:2]) if len(parts) >= 2 else "root"
        grouped.setdefault(group, {})[key] = value
    return grouped


def write_messages_dir(base_dir: Path, payload_content: dict[str, Any]) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    grouped = group_messages(payload_content)
    existing = {path.stem for path in base_dir.glob("*.json")}
    desired = set(grouped.keys())
    for name in existing - desired:
        (base_dir / f"{name}.json").unlink()
    for name, entries in grouped.items():
        target_path = base_dir / f"{name}.json"
        target_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_messages_target(messages_map: dict[str, str], lang: str) -> str:
    if lang in messages_map:
        return messages_map[lang]
    if (PACKAGE_ROOT / "messages" / lang).exists():
        return f"messages/{lang}"
    return f"messages_{lang}.json"
