from __future__ import annotations

from pathlib import Path


def get_env_vars() -> dict[str, str]:
    env_path = Path(".env")
    if not env_path.exists():
        return {}
    result: dict[str, str] = {}
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


def persist_env_vars(updates: dict[str, str]) -> None:
    from dotenv import set_key

    env_path = Path(".env")
    env_path.touch(exist_ok=True)
    for key, value in updates.items():
        set_key(env_path, key, value)
