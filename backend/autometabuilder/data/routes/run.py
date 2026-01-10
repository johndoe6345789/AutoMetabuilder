"""Run route for triggering the bot."""
from __future__ import annotations

from flask import Blueprint, request

from autometabuilder.data.run_state import start_bot

run_bp = Blueprint("run", __name__)


@run_bp.route("/api/run", methods=["POST"])
def api_run() -> tuple[dict[str, object], int]:
    payload = request.get_json(silent=True) or {}
    mode = payload.get("mode", "once")
    iterations = int(payload.get("iterations", 1))
    yolo = bool(payload.get("yolo", True))
    stop_at_mvp = bool(payload.get("stop_at_mvp", False))
    started = start_bot(mode, iterations, yolo, stop_at_mvp)
    return {"started": started}, 202 if started else 409
