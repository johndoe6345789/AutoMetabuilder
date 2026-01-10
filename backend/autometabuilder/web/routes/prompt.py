"""Prompt and workflow editing routes."""
from __future__ import annotations

from flask import Blueprint, request

from ..data import build_prompt_yaml, write_prompt, write_workflow

prompt_bp = Blueprint("prompt", __name__)


@prompt_bp.route("/api/prompt", methods=["POST"])
def api_prompt() -> tuple[dict[str, str], int]:
    payload = request.get_json(force=True)
    content = payload.get("content")
    system = payload.get("system_content")
    user = payload.get("user_content")
    model = payload.get("model")
    mode = payload.get("prompt_mode", "builder")
    if mode == "raw" and content is not None:
        write_prompt(content)
    else:
        write_prompt(build_prompt_yaml(system, user, model))
    return {"status": "ok"}, 200


@prompt_bp.route("/api/workflow", methods=["POST"])
def api_workflow() -> tuple[dict[str, str], int]:
    payload = request.get_json(force=True)
    write_workflow(payload.get("content", ""))
    return {"status": "saved"}, 200
