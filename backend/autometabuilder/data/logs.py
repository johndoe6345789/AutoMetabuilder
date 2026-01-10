from __future__ import annotations

from .paths import LOG_FILE


def get_recent_logs(lines: int = 50) -> str:
    if not LOG_FILE.exists():
        return ""
    with LOG_FILE.open("r", encoding="utf-8") as handle:
        content = handle.readlines()
    return "".join(content[-lines:])
