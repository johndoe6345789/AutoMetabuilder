"""Workflow plugin: register Flask blueprint."""
from .....utils import load_callable


def run(runtime, inputs):
    """
    Register a Flask blueprint with the Flask app.
    
    Inputs:
        blueprint_path: Dotted path to the blueprint (e.g., "autometabuilder.data.routes.context.context_bp")
        blueprint: Direct blueprint object (alternative to blueprint_path)
        
    Returns:
        dict: Success indicator
    """
    app = runtime.context.get("flask_app")
    if not app:
        return {"error": "Flask app not found in context. Run web.create_flask_app first."}
    
    # Try direct blueprint first
    blueprint = inputs.get("blueprint")
    
    # Otherwise load from path
    if not blueprint:
        blueprint_path = inputs.get("blueprint_path")
        if not blueprint_path:
            return {"error": "blueprint or blueprint_path is required"}
        
        try:
            blueprint = load_callable(blueprint_path)
        except Exception as e:
            return {"error": f"Failed to load blueprint: {str(e)}"}
    
    try:
        app.register_blueprint(blueprint)
        return {"result": f"Blueprint {blueprint.name} registered"}
    except Exception as e:
        return {"error": f"Failed to register blueprint: {str(e)}"}
