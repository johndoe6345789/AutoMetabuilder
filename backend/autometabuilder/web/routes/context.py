"""Context routes for dashboard state and logs."""
from __future__ import annotations

import os

from flask import Blueprint

from ..data import (
    get_env_vars,
    get_navigation_items,
    get_prompt_content,
    get_recent_logs,
    get_ui_messages,
    get_workflow_content,
    list_translations,
    load_metadata,
    load_workflow_packages,
    summarize_workflow_packages,
)
from ..run_state import bot_process, current_run_config, mock_running
from autometabuilder.roadmap_utils import is_mvp_reached

context_bp = Blueprint("context", __name__)


def build_context() -> dict[str, object]:
    lang = os.environ.get("APP_LANG", "en")
    metadata = load_metadata()
    packages = load_workflow_packages()
    return {
        "logs": get_recent_logs(),
        "env_vars": get_env_vars(),
        "translations": list_translations(),
        "metadata": metadata,
        "navigation": get_navigation_items(),
        "prompt_content": get_prompt_content(),
        "workflow_content": get_workflow_content(),
        "workflow_packages": summarize_workflow_packages(packages),
        "workflow_packages_raw": packages,
        "messages": get_ui_messages(lang),
        "lang": lang,
        "status": {
            "is_running": bot_process is not None or mock_running,
            "mvp_reached": is_mvp_reached(),
            "config": current_run_config,
        },
    }


@context_bp.route("/api/context")
def api_context() -> tuple[dict[str, object], int]:
    return build_context(), 200


@context_bp.route("/api/status")
def api_status() -> tuple[dict[str, object], int]:
    return build_context()["status"], 200


@context_bp.route("/api/logs")
def api_logs() -> tuple[dict[str, str], int]:
    return {"logs": get_recent_logs()}, 200
