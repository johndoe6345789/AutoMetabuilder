from __future__ import annotations

import json
import shutil
from typing import Any

from .messages_io import load_messages, resolve_messages_target, write_messages_dir
from .metadata import get_messages_map, load_metadata_base, write_metadata
from .paths import PACKAGE_ROOT

def load_translation(lang: str) -> dict[str, Any]:
    messages_map = get_messages_map()
    target = resolve_messages_target(messages_map, lang)
    if not target:
        return {}
    return load_messages(PACKAGE_ROOT / target)


def list_translations() -> dict[str, str]:
    messages_map = get_messages_map()
    if messages_map:
        return messages_map
    fallback = {}
    for candidate in PACKAGE_ROOT.glob("messages_*.json"):
        name = candidate.name
        language = name.removeprefix("messages_").removesuffix(".json")
        fallback[language] = name
    messages_dir = PACKAGE_ROOT / "messages"
    if messages_dir.exists():
        for candidate in messages_dir.iterdir():
            if candidate.is_dir():
                fallback[candidate.name] = f"messages/{candidate.name}"
    return fallback


def get_ui_messages(lang: str) -> dict[str, Any]:
    messages_map = get_messages_map()
    base_name = resolve_messages_target(messages_map, "en")
    base = load_messages(PACKAGE_ROOT / base_name)
    localized = load_messages(PACKAGE_ROOT / resolve_messages_target(messages_map, lang))
    merged = dict(base)
    merged.update(localized)
    merged["__lang"] = lang
    return merged


def create_translation(lang: str) -> bool:
    messages_map = get_messages_map()
    if lang in messages_map:
        return False
    base = resolve_messages_target(messages_map, "en")
    base_file = PACKAGE_ROOT / base
    if not base_file.exists():
        return False
    if base_file.is_dir():
        target_name = f"messages/{lang}"
        target_path = PACKAGE_ROOT / target_name
        shutil.copytree(base_file, target_path)
    else:
        target_name = f"messages_{lang}.json"
        target_path = PACKAGE_ROOT / target_name
        shutil.copy(base_file, target_path)
    messages_map[lang] = target_name
    metadata = load_metadata_base()
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
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    del messages_map[lang]
    metadata = load_metadata_base()
    metadata["messages"] = messages_map
    write_metadata(metadata)
    return True


def update_translation(lang: str, payload: dict[str, Any]) -> bool:
    messages_map = get_messages_map()
    if lang not in messages_map:
        return False
    payload_content = payload.get("content", {})
    target_path = PACKAGE_ROOT / messages_map[lang]
    if target_path.is_dir():
        write_messages_dir(target_path, payload_content)
    else:
        target_path.write_text(json.dumps(payload_content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True
