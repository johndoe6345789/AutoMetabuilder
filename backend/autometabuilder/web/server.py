"""Flask-based API surface that replaces the legacy FastAPI frontend."""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from typing import Dict

from flask import Flask, request

from ..roadmap_utils import is_mvp_reached
from .data import (
    build_prompt_yaml,
    create_translation,
    delete_translation,
    get_env_vars,
    get_navigation_items,
    get_prompt_content,
    get_recent_logs,
    get_ui_messages,
    get_workflow_content,
    list_translations,
    load_metadata,
    load_translation,
    load_workflow_packages,
    persist_env_vars,
    summarize_workflow_packages,
    update_translation,
    write_prompt,
    write_workflow,
)
from .workflow_graph import build_workflow_graph

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

bot_process = None
mock_running = False
current_run_config: Dict[str, object] = {}


def _reset_run_state() -> None:
    global bot_process, current_run_config
    bot_process = None
    current_run_config = {}


def run_bot_task(mode: str, iterations: int, yolo: bool, stop_at_mvp: bool) -> None:
    global bot_process, mock_running, current_run_config
    current_run_config = {
        "mode": mode,
        "iterations": iterations,
        "yolo": yolo,
        "stop_at_mvp": stop_at_mvp,
    }

    if os.environ.get("MOCK_WEB_UI") == "true":
        mock_running = True
        time.sleep(5)
        mock_running = False
        _reset_run_state()
        return

    try:
        cmd = [sys.executable, "-m", "autometabuilder.main"]
        if yolo:
            cmd.append("--yolo")
        if mode == "once":
            cmd.append("--once")
        if mode == "iterations" and iterations > 1:
            for _ in range(iterations):
                if stop_at_mvp and is_mvp_reached():
                    break
                bot_process = subprocess.Popen(cmd + ["--once"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                bot_process.wait()
        else:
            bot_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            bot_process.wait()
    finally:
        _reset_run_state()


def start_bot(mode: str = "once", iterations: int = 1, yolo: bool = True, stop_at_mvp: bool = False) -> bool:
    if bot_process is not None or mock_running:
        return False
    thread = threading.Thread(target=run_bot_task, args=(mode, iterations, yolo, stop_at_mvp), daemon=True)
    thread.start()
    return True


def build_context() -> Dict[str, object]:
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


@app.route("/api/context")
def api_context() -> tuple[Dict[str, object], int]:
    return build_context(), 200


@app.route("/api/run", methods=["POST"])
def api_run() -> tuple[Dict[str, object], int]:
    payload = request.get_json(silent=True) or {}
    mode = payload.get("mode", "once")
    iterations = int(payload.get("iterations", 1))
    yolo = bool(payload.get("yolo", True))
    stop_at_mvp = bool(payload.get("stop_at_mvp", False))
    started = start_bot(mode, iterations, yolo, stop_at_mvp)
    return {"started": started}, 202 if started else 409


@app.route("/api/prompt", methods=["POST"])
def api_prompt() -> tuple[Dict[str, str], int]:
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


@app.route("/api/workflow", methods=["POST"])
def api_workflow() -> tuple[Dict[str, str], int]:
    payload = request.get_json(force=True)
    write_workflow(payload.get("content", ""))
    return {"status": "saved"}, 200


@app.route("/api/settings", methods=["POST"])
def api_settings() -> tuple[Dict[str, str], int]:
    payload = request.get_json(force=True) or {}
    entries = payload.get("env", {}) or {}
    persist_env_vars(entries)
    return {"status": "ok"}, 200


@app.route("/api/status")
def api_status() -> tuple[Dict[str, object], int]:
    return build_context()["status"], 200


@app.route("/api/logs")
def api_logs() -> tuple[Dict[str, str], int]:
    return {"logs": get_recent_logs()}, 200


@app.route("/api/translation-options")
def api_translation_options() -> tuple[Dict[str, Dict[str, str]], int]:
    return {"translations": list_translations()}, 200


@app.route("/api/translations", methods=["POST"])
def api_create_translation() -> tuple[Dict[str, str], int]:
    payload = request.get_json(force=True)
    lang = payload.get("lang")
    if not lang:
        return {"error": "lang required"}, 400
    ok = create_translation(lang)
    return ({"created": ok}, 201 if ok else 400)


@app.route("/api/translations/<lang>", methods=["GET"])
def api_get_translation(lang: str) -> tuple[Dict[str, object], int]:
    if lang not in load_metadata().get("messages", {}):
        return {"error": "translation not found"}, 404
    return {"lang": lang, "content": load_translation(lang)}, 200


@app.route("/api/translations/<lang>", methods=["PUT"])
def api_update_translation(lang: str) -> tuple[Dict[str, str], int]:
    payload = request.get_json(force=True)
    updated = update_translation(lang, payload)
    if not updated:
        return {"error": "unable to update"}, 400
    return {"status": "saved"}, 200


@app.route("/api/translations/<lang>", methods=["DELETE"])
def api_delete_translation(lang: str) -> tuple[Dict[str, str], int]:
    deleted = delete_translation(lang)
    if not deleted:
        return {"error": "cannot delete"}, 400
    return {"deleted": True}, 200


@app.route("/api/navigation")
def api_navigation() -> tuple[Dict[str, object], int]:
    return {"items": get_navigation_items()}, 200


@app.route("/api/workflow/plugins")
def api_workflow_plugins() -> tuple[Dict[str, object], int]:
    return {"plugins": load_metadata().get("workflow_plugins", {})}, 200


@app.route("/api/workflow/packages")
def api_workflow_packages() -> tuple[Dict[str, object], int]:
    packages = load_workflow_packages()
    return {"packages": summarize_workflow_packages(packages)}, 200


@app.route("/api/workflow/packages/<package_id>")
def api_get_workflow_package(package_id: str) -> tuple[Dict[str, object], int]:
    packages = load_workflow_packages()
    for pkg in packages:
        if pkg.get("id") == package_id:
            return pkg, 200
    return {"error": "package not found"}, 404


@app.route("/api/workflow/graph")
def api_workflow_graph() -> tuple[Dict[str, object], int]:
    return build_workflow_graph(), 200


def start_web_ui(host: str = "0.0.0.0", port: int = 8000) -> None:
    app.run(host=host, port=port)
