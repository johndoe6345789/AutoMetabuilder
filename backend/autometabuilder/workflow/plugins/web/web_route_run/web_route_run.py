"""Workflow plugin: run API routes blueprint."""
from flask import Blueprint, jsonify, request
from autometabuilder.data.run_state import start_bot


def run(runtime, _inputs):
    """Create and return the run routes blueprint."""
    run_bp = Blueprint("run", __name__)
    
    @run_bp.route("/api/run", methods=["POST"])
    def api_run_bot():
        payload = request.get_json(force=True)
        mode = payload.get("mode", "once")
        iterations = payload.get("iterations", 1)
        yolo = payload.get("yolo", True)
        stop_at_mvp = payload.get("stop_at_mvp", False)
        
        started = start_bot(mode, iterations, yolo, stop_at_mvp)
        if not started:
            return jsonify({"error": "Bot already running"}), 400
        
        return jsonify({"status": "started"}), 200
    
    # Store in runtime context and return
    runtime.context["run_bp"] = run_bp
    return {"result": run_bp, "blueprint_path": "run_bp"}
