"""Workflow plugin: settings API routes blueprint."""
from flask import Blueprint, jsonify, request


def run(runtime, _inputs):
    """Create and return the settings routes blueprint."""
    settings_bp = Blueprint("settings", __name__)
    
    @settings_bp.route("/api/settings", methods=["POST"])
    def api_update_settings():
        from autometabuilder.data import persist_env_vars
        payload = request.get_json(force=True)
        env_vars = payload.get("env_vars", {})
        persist_env_vars(env_vars)
        return jsonify({"status": "saved"}), 200
    
    # Store in runtime context and return
    runtime.context["settings_bp"] = settings_bp
    return {"result": settings_bp, "blueprint_path": "settings_bp"}
