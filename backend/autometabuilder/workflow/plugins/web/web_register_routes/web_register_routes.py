"""Workflow plugin: register routes from JSON configuration."""
from flask import Blueprint, jsonify, request


def run(runtime, inputs):
    """
    Register routes from JSON configuration.
    
    This allows routes to be defined declaratively in the workflow JSON
    rather than in Python code.
    
    Inputs:
        blueprint_name: Name for the blueprint (required)
        routes: List of route configurations (required)
            Each route should have:
            - path: The URL path (e.g., "/api/navigation")
            - methods: List of HTTP methods (default: ["GET"])
            - handler: Name of the handler function or plugin to call
            - handler_type: "plugin" or "function" (default: "plugin")
            - handler_inputs: Inputs to pass to the plugin/function (optional)
    
    Returns:
        dict: Contains the blueprint in result
    """
    app = runtime.context.get("flask_app")
    if not app:
        return {"error": "Flask app not found in context. Run web.create_flask_app first."}
    
    blueprint_name = inputs.get("blueprint_name")
    if not blueprint_name:
        return {"error": "blueprint_name is required"}
    
    routes = inputs.get("routes", [])
    if not routes:
        return {"error": "routes list is required"}
    
    # Create blueprint
    blueprint = Blueprint(blueprint_name, __name__)
    
    # Register each route
    for route_config in routes:
        path = route_config.get("path")
        if not path:
            runtime.logger.error(f"Route missing 'path' in {blueprint_name}")
            continue
        
        methods = route_config.get("methods", ["GET"])
        handler = route_config.get("handler")
        handler_type = route_config.get("handler_type", "plugin")
        handler_inputs = route_config.get("handler_inputs", {})
        
        if not handler:
            runtime.logger.error(f"Route {path} missing 'handler' in {blueprint_name}")
            continue
        
        # Create route handler function
        def make_handler(handler_name, h_type, h_inputs):
            """Create a handler function with captured variables."""
            def route_handler():
                try:
                    if h_type == "plugin":
                        # Execute plugin and return result
                        from autometabuilder.workflow.plugin_registry import load_plugin_map, PluginRegistry
                        plugin_map = load_plugin_map()
                        registry = PluginRegistry(plugin_map)
                        plugin = registry.get(handler_name)
                        
                        if not plugin:
                            return jsonify({"error": f"Plugin {handler_name} not found"}), 500
                        
                        # Merge handler inputs with any request data
                        inputs_copy = dict(h_inputs)
                        if request.method == "POST" and request.is_json:
                            inputs_copy.update(request.get_json())
                        
                        result = plugin(runtime, inputs_copy)
                        
                        # If result has a "result" key, return that
                        if isinstance(result, dict) and "result" in result:
                            return jsonify(result["result"]), 200
                        
                        return jsonify(result), 200
                    else:
                        # For function type, could load and call a function
                        return jsonify({"error": "Function handler type not yet implemented"}), 500
                        
                except Exception as e:
                    runtime.logger.error(f"Error in route handler {path}: {e}")
                    return jsonify({"error": str(e)}), 500
            
            return route_handler
        
        # Add route to blueprint
        handler_func = make_handler(handler, handler_type, handler_inputs)
        handler_func.__name__ = f"{blueprint_name}_{path.replace('/', '_')}"
        blueprint.add_url_rule(path, view_func=handler_func, methods=methods)
    
    # Register blueprint with app
    app.register_blueprint(blueprint)
    
    return {
        "result": blueprint,
        "message": f"Registered blueprint '{blueprint_name}' with {len(routes)} routes"
    }
