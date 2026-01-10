"""Workflow plugin: context API routes blueprint."""
import os
from flask import Blueprint, jsonify
from autometabuilder.loaders.metadata_loader import load_metadata
from autometabuilder.data.run_state import bot_process, current_run_config, mock_running
from autometabuilder.roadmap_utils import is_mvp_reached


def run(runtime, _inputs):
    """Create and return the context routes blueprint."""
    context_bp = Blueprint("context", __name__)
    
    def build_context():
        """Build complete context for API."""
        from autometabuilder.data import (
            get_env_vars,
            get_navigation_items,
            get_prompt_content,
            get_recent_logs,
            get_ui_messages,
            get_workflow_content,
            list_translations,
            load_workflow_packages,
            summarize_workflow_packages,
        )
        
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
    def api_context():
        return jsonify(build_context()), 200
    
    @context_bp.route("/api/status")
    def api_status():
        return jsonify(build_context()["status"]), 200
    
    @context_bp.route("/api/logs")
    def api_logs():
        from autometabuilder.data import get_recent_logs
        return jsonify({"logs": get_recent_logs()}), 200
    
    # Store in runtime context and return
    runtime.context["context_bp"] = context_bp
    return {"result": context_bp, "blueprint_path": "context_bp"}
