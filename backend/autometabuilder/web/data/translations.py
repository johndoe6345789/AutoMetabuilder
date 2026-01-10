from __future__ import annotations

import json
import shutil
from typing import Any

from .json_utils import read_json
from .metadata import get_messages_map, load_metadata, write_metadata
from .paths import PACKAGE_ROOT


def load_translation(lang: str) -> dict[str, Any]:
    messages_map = get_messages_map()
    target = messages_map.get(lang)
    if not target:
        return {}
    return read_json(PACKAGE_ROOT / target)


def list_translations() -> dict[str, str]:
    messages_map = get_messages_map()
    if messages_map:
        return messages_map
    fallback = {}
    for candidate in PACKAGE_ROOT.glob("messages_*.json"):
        name = candidate.name
        language = name.removeprefix("messages_").removesuffix(".json")
        fallback[language] = name
    return fallback


def get_ui_messages(lang: str) -> dict[str, Any]:
    messages_map = get_messages_map()
    base_name = messages_map.get("en", "messages_en.json")
    base = read_json(PACKAGE_ROOT / base_name)
    localized = read_json(PACKAGE_ROOT / messages_map.get(lang, base_name))
    merged = dict(base)
    merged.update(localized)
    merged["__lang"] = lang
    return merged


def create_translation(lang: str) -> bool:
    messages_map = get_messages_map()
    if lang in messages_map:
        return False
    base = messages_map.get("en", "messages_en.json")
    base_file = PACKAGE_ROOT / base
    if not base_file.exists():
        return False
    target_name = f"messages_{lang}.json"
    target_path = PACKAGE_ROOT / target_name
    shutil.copy(base_file, target_path)
    messages_map[lang] = target_name
    metadata = load_metadata()
    metadata["messages"] = messages_map
    write_metadata(metadata)
    return True


def delete_translation(lang: str) -> bool:
    if lang == "en":
        return False
    messages_map = get_messages_map()
    if lang not in messages_map:
        return False
    target = PACKAGE_ROOT / messages_map[lang]
    if target.exists():
        target.unlink()
    del messages_map[lang]
    metadata = load_metadata()
    metadata["messages"] = messages_map
    write_metadata(metadata)
    return True


def update_translation(lang: str, payload: dict[str, Any]) -> bool:
    messages_map = get_messages_map()
    if lang not in messages_map:
        return False
    payload_content = payload.get("content", {})
    target_path = PACKAGE_ROOT / messages_map[lang]
    target_path.write_text(json.dumps(payload_content, indent=2, ensure_ascii=False), encoding="utf-8")
    return True
