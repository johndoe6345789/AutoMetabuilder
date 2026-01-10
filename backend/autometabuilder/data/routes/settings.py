"""Settings persistence route."""
from __future__ import annotations

from flask import Blueprint, request

from autometabuilder.data import persist_env_vars

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/api/settings", methods=["POST"])
def api_settings() -> tuple[dict[str, str], int]:
    payload = request.get_json(force=True) or {}
    entries = payload.get("env", {}) or {}
    persist_env_vars(entries)
    return {"status": "ok"}, 200
