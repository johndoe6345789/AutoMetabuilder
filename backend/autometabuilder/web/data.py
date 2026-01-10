"""Helpers for loading metadata, translations, and workflow assets."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parent.parent
LOG_FILE = REPO_ROOT / "autometabuilder.log"


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_prompt_yaml(system_content: str | None, user_content: str | None, model: str | None) -> str:
    def indent_block(text: str | None) -> str:
        if not text:
            return ""
        return "\n      ".join(line.rstrip() for line in text.splitlines())

    model_value = model or "openai/gpt-4o"
    system_block = indent_block(system_content)
    user_block = indent_block(user_content)
    return f"""messages:
  - role: system
    content: >-
      {system_block}
  - role: user
    content: >-
      {user_block}
model: {model_value}
"""


def load_metadata() -> Dict[str, Any]:
    metadata_path = PACKAGE_ROOT / "metadata.json"
    return _read_json(metadata_path)


def write_metadata(metadata: Dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "metadata.json"
    path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def get_messages_map(metadata: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    metadata = metadata or load_metadata()
    return metadata.get("messages", {})


def load_translation(lang: str) -> Dict[str, Any]:
    messages_map = get_messages_map()
    target = messages_map.get(lang)
    if not target:
        return {}
    return _read_json(PACKAGE_ROOT / target)


def list_translations() -> Dict[str, str]:
    messages_map = get_messages_map()
    if messages_map:
        return messages_map
    # falling back to files on disk
    fallback = {}
    for candidate in PACKAGE_ROOT.glob("messages_*.json"):
        name = candidate.name
        language = name.removeprefix("messages_").removesuffix(".json")
        fallback[language] = name
    return fallback


def get_ui_messages(lang: str) -> Dict[str, Any]:
    messages_map = get_messages_map()
    base_name = messages_map.get("en", "messages_en.json")
    base = _read_json(PACKAGE_ROOT / base_name)
    localized = _read_json(PACKAGE_ROOT / messages_map.get(lang, base_name))
    merged = dict(base)
    merged.update(localized)
    merged["__lang"] = lang
    return merged


def get_prompt_content() -> str:
    path = Path(os.environ.get("PROMPT_PATH", "prompt.yml"))
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def write_prompt(content: str) -> None:
    path = Path(os.environ.get("PROMPT_PATH", "prompt.yml"))
    path.write_text(content or "", encoding="utf-8")


def get_workflow_content() -> str:
    metadata = load_metadata()
    workflow_name = metadata.get("workflow_path", "workflow.json")
    workflow_path = PACKAGE_ROOT / workflow_name
    if workflow_path.exists():
        return workflow_path.read_text(encoding="utf-8")
    return ""


def write_workflow(content: str) -> None:
    metadata = load_metadata()
    workflow_name = metadata.get("workflow_path", "workflow.json")
    workflow_path = PACKAGE_ROOT / workflow_name
    workflow_path.write_text(content or "", encoding="utf-8")


def get_navigation_items() -> List[Dict[str, Any]]:
    nav_path = PACKAGE_ROOT / "web" / "navigation_items.json"
    nav = _read_json(nav_path)
    if isinstance(nav, list):
        return nav
    return []


def get_workflow_packages_dir() -> Path:
    metadata = load_metadata()
    packages_name = metadata.get("workflow_packages_path", "workflow_packages")
    return PACKAGE_ROOT / packages_name


def load_workflow_packages() -> List[Dict[str, Any]]:
    packages_dir = get_workflow_packages_dir()
    if not packages_dir.exists():
        return []
    packages: List[Dict[str, Any]] = []
    for file in sorted(packages_dir.iterdir()):
        if file.suffix != ".json":
            continue
        data = _read_json(file)
        if not isinstance(data, dict):
            continue
        pkg_id = data.get("id") or file.stem
        data["id"] = pkg_id
        data.setdefault("workflow", {"nodes": []})
        packages.append(data)
    return packages


def summarize_workflow_packages(packages: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    summary = []
    for pkg in packages:
        summary.append(
            {
                "id": pkg["id"],
                "label": pkg.get("label") or pkg["id"],
                "description": pkg.get("description", ""),
                "tags": pkg.get("tags", []),
            }
        )
    return summary


def get_env_vars() -> Dict[str, str]:
    env_path = Path(".env")
    if not env_path.exists():
        return {}
    result: Dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip("'\"")
        result[key.strip()] = value
    return result


def persist_env_vars(updates: Dict[str, str]) -> None:
    from dotenv import set_key

    env_path = Path(".env")
    env_path.touch(exist_ok=True)
    for key, value in updates.items():
        set_key(env_path, key, value)


def get_recent_logs(lines: int = 50) -> str:
    if not LOG_FILE.exists():
        return ""
    with LOG_FILE.open("r", encoding="utf-8") as handle:
        content = handle.readlines()
    return "".join(content[-lines:])


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


def update_translation(lang: str, payload: Dict[str, Any]) -> bool:
    messages_map = get_messages_map()
    if lang not in messages_map:
        return False
    payload_content = payload.get("content", {})
    target_path = PACKAGE_ROOT / messages_map[lang]
    target_path.write_text(json.dumps(payload_content, indent=2, ensure_ascii=False), encoding="utf-8")
    return True
