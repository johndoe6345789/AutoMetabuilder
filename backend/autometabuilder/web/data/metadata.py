from __future__ import annotations

import json
from typing import Any

from .json_utils import read_json
from .paths import PACKAGE_ROOT


def load_metadata() -> dict[str, Any]:
    metadata_path = PACKAGE_ROOT / "metadata.json"
    return read_json(metadata_path)


def write_metadata(metadata: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "metadata.json"
    path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def get_messages_map(metadata: dict[str, Any] | None = None) -> dict[str, str]:
    metadata = metadata or load_metadata()
    return metadata.get("messages", {})
