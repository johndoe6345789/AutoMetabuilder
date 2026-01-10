"""Workflow plugin: run API routes blueprint."""
from flask import Blueprint, jsonify, request
from autometabuilder.workflow.plugin_loader import load_plugin_callable

# Cache the start_bot plugin callable to avoid repeated loading
_start_bot_plugin = None


def run(runtime, _inputs):
    """Create and return the run routes blueprint."""
    global _start_bot_plugin
    
    # Load the control.start_bot plugin once
    if _start_bot_plugin is None:
        _start_bot_plugin = load_plugin_callable(
            "autometabuilder.workflow.plugins.control.control_start_bot.control_start_bot.run"
        )
    
    run_bp = Blueprint("run", __name__)
    
    @run_bp.route("/api/run", methods=["POST"])
    def api_run_bot():
        payload = request.get_json(force=True)
        mode = payload.get("mode", "once")
        iterations = payload.get("iterations", 1)
        yolo = payload.get("yolo", True)
        stop_at_mvp = payload.get("stop_at_mvp", False)
        
        # Call the control.start_bot plugin
        result = _start_bot_plugin(runtime, {
            "mode": mode,
            "iterations": iterations,
            "yolo": yolo,
            "stop_at_mvp": stop_at_mvp
        })
        
        if not result.get("started"):
            return jsonify({"error": result.get("error", "Bot already running")}), 400
        
        return jsonify({"status": "started"}), 200
    
    # Store in runtime context and return
    runtime.context["run_bp"] = run_bp
    return {"result": run_bp, "blueprint_path": "run_bp"}
