"""Workflow plugin: register Flask blueprint."""


def run(runtime, inputs):
    """
    Register a Flask blueprint with the Flask app.
    
    Inputs:
        blueprint_path: Dotted path to the blueprint (e.g., "autometabuilder.web.routes.context.context_bp")
        
    Returns:
        dict: Success indicator
    """
    from ....loaders.callable_loader import load_callable
    
    app = runtime.context.get("flask_app")
    if not app:
        return {"error": "Flask app not found in context. Run web.create_flask_app first."}
    
    blueprint_path = inputs.get("blueprint_path")
    if not blueprint_path:
        return {"error": "blueprint_path is required"}
    
    try:
        blueprint = load_callable(blueprint_path)
        app.register_blueprint(blueprint)
        return {"result": f"Blueprint {blueprint_path} registered"}
    except Exception as e:
        return {"error": f"Failed to register blueprint: {str(e)}"}
