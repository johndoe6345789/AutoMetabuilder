from __future__ import annotations

import json
from typing import Any

from autometabuilder.metadata_loader import load_metadata as load_metadata_full
from .json_utils import read_json
from .paths import PACKAGE_ROOT


def load_metadata() -> dict[str, Any]:
    return load_metadata_full()


def load_metadata_base() -> dict[str, Any]:
    metadata_path = PACKAGE_ROOT / "metadata.json"
    return read_json(metadata_path)


def write_metadata(metadata: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "metadata.json"
    path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def get_messages_map(metadata: dict[str, Any] | None = None) -> dict[str, str]:
    metadata = metadata or load_metadata_base()
    return metadata.get("messages", {})
