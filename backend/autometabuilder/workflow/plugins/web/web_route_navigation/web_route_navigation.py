"""Workflow plugin: navigation API routes blueprint."""
from flask import Blueprint, jsonify
from autometabuilder.loaders.metadata_loader import load_metadata
from autometabuilder.data.workflow_graph import build_workflow_graph


def run(runtime, _inputs):
    """Create and return the navigation routes blueprint."""
    navigation_bp = Blueprint("navigation", __name__)
    
    @navigation_bp.route("/api/navigation")
    def api_navigation():
        from autometabuilder.data import get_navigation_items
        return jsonify({"navigation": get_navigation_items()}), 200
    
    @navigation_bp.route("/api/workflow/packages")
    def api_workflow_packages():
        from autometabuilder.data import load_workflow_packages, summarize_workflow_packages
        packages = load_workflow_packages()
        return jsonify({"packages": summarize_workflow_packages(packages)}), 200
    
    @navigation_bp.route("/api/workflow/plugins")
    def api_workflow_plugins():
        metadata = load_metadata()
        plugins = metadata.get("workflow_plugins", {})
        return jsonify({"plugins": plugins}), 200
    
    @navigation_bp.route("/api/workflow/graph")
    def api_workflow_graph():
        graph = build_workflow_graph()
        return jsonify(graph), 200
    
    # Store in runtime context and return
    runtime.context["navigation_bp"] = navigation_bp
    return {"result": navigation_bp, "blueprint_path": "navigation_bp"}
