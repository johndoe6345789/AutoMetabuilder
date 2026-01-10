from __future__ import annotations

from typing import Any

from .json_utils import read_json
from .paths import PACKAGE_ROOT


def get_navigation_items() -> list[dict[str, Any]]:
    nav_path = PACKAGE_ROOT / "web" / "navigation_items.json"
    nav = read_json(nav_path)
    if isinstance(nav, list):
        return nav
    return []
