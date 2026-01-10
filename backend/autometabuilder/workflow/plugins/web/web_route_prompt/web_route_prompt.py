"""Workflow plugin: prompt API routes blueprint."""
from flask import Blueprint, jsonify, request


def run(runtime, _inputs):
    """Create and return the prompt routes blueprint."""
    prompt_bp = Blueprint("prompt", __name__)
    
    @prompt_bp.route("/api/prompt", methods=["POST"])
    def api_save_prompt():
        from autometabuilder.data import build_prompt_yaml, write_prompt
        payload = request.get_json(force=True)
        system_content = payload.get("system")
        user_content = payload.get("user")
        model = payload.get("model")
        
        content = build_prompt_yaml(system_content, user_content, model)
        write_prompt(content)
        return jsonify({"status": "saved"}), 200
    
    @prompt_bp.route("/api/workflow", methods=["POST"])
    def api_save_workflow():
        from autometabuilder.data import write_workflow
        payload = request.get_json(force=True)
        content = payload.get("content", "")
        write_workflow(content)
        return jsonify({"status": "saved"}), 200
    
    # Store in runtime context and return
    runtime.context["prompt_bp"] = prompt_bp
    return {"result": prompt_bp, "blueprint_path": "prompt_bp"}
