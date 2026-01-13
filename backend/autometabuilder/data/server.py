"""Server module for UI tests - creates a minimal Flask app for testing."""
import os
import logging
from flask import Flask, send_from_directory, jsonify
from asgiref.wsgi import WsgiToAsgi
from autometabuilder.workflow.plugin_registry import PluginRegistry, load_plugin_map
from autometabuilder.workflow.runtime import WorkflowRuntime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _SimpleLogger:
    """Minimal logger for plugin execution."""
    def info(self, *args, **kwargs):
        logger.info(*args, **kwargs)
    
    def debug(self, *args, **kwargs):
        logger.debug(*args, **kwargs)
    
    def error(self, *args, **kwargs):
        logger.error(*args, **kwargs)


def create_app():
    """Create and configure the Flask application for testing."""
    # Create Flask app
    app = Flask(__name__, static_folder=None)
    app.config['JSON_SORT_KEYS'] = False
    
    # Create runtime for plugin execution
    runtime = WorkflowRuntime(
        context={},
        store={},
        tool_runner=None,
        logger=_SimpleLogger()
    )
    
    # Store Flask app in runtime context
    runtime.context["flask_app"] = app
    
    # Load plugins
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    
    # Check if we're in mock mode (for testing)
    mock_mode = os.environ.get("MOCK_WEB_UI", "false").lower() == "true"
    
    if mock_mode:
        # Create minimal mock routes for testing
        @app.route('/')
        def index():
            # Return a minimal HTML page for testing
            return '''<!DOCTYPE html>
<html>
<head><title>AutoMetabuilder</title></head>
<body>
<div id="dashboard" class="active">
    <h1>Dashboard</h1>
    <button id="run-btn">Run</button>
    <div id="status-indicator">Ready</div>
</div>
<div id="workflow"></div>
<div id="prompt"></div>
<div id="settings"></div>
<div id="translations"></div>
<nav data-section="dashboard">Dashboard</nav>
<nav data-section="workflow">Workflow</nav>
<nav data-section="prompt">Prompt</nav>
<nav data-section="settings">Settings</nav>
<nav data-section="translations">Translations</nav>
<div class="amb-sidebar-footer">testuser</div>
</body>
</html>''', 200
        
        @app.route('/<path:path>')
        def serve_static(path):
            # Redirect to index for all routes in mock mode
            return index()
        
        @app.route('/api/context')
        def api_context():
            from autometabuilder.utils import load_metadata
            return jsonify({
                "logs": [],
                "env_vars": {},
                "translations": ["en"],
                "metadata": load_metadata(),
                "navigation": [],
                "prompt_content": "",
                "workflow_content": "",
                "workflow_packages": [],
                "workflow_packages_raw": [],
                "messages": {},
                "lang": os.environ.get("APP_LANG", "en"),
                "status": {
                    "is_running": False,
                    "mvp_reached": False,
                    "config": {}
                }
            }), 200
        
        @app.route('/api/status')
        def api_status():
            return jsonify({
                "is_running": False,
                "mvp_reached": False,
                "config": {}
            }), 200
        
        @app.route('/api/run', methods=['POST'])
        def api_run():
            return jsonify({"success": True, "message": "Mock run"}), 200
        
    else:
        # Create routes using workflow plugins
        try:
            # Create context routes
            context_result = registry.get("web.route_context")(runtime, {})
            context_bp = context_result.get("result")
            if context_bp:
                app.register_blueprint(context_bp)
            
            # Create run routes
            run_result = registry.get("web.route_run")(runtime, {})
            run_bp = run_result.get("result")
            if run_bp:
                app.register_blueprint(run_bp)
            
            # Create prompt routes
            prompt_result = registry.get("web.route_prompt")(runtime, {})
            prompt_bp = prompt_result.get("result")
            if prompt_bp:
                app.register_blueprint(prompt_bp)
            
            # Create settings routes
            settings_result = registry.get("web.route_settings")(runtime, {})
            settings_bp = settings_result.get("result")
            if settings_bp:
                app.register_blueprint(settings_bp)
            
            # Create translations routes
            translations_result = registry.get("web.route_translations")(runtime, {})
            translations_bp = translations_result.get("result")
            if translations_bp:
                app.register_blueprint(translations_bp)
            
            # Create navigation routes
            navigation_result = registry.get("web.route_navigation")(runtime, {})
            navigation_bp = navigation_result.get("result")
            if navigation_bp:
                app.register_blueprint(navigation_bp)
            
            # Serve static files
            from pathlib import Path
            frontend_dist = Path(__file__).resolve().parent.parent.parent.parent / 'frontend' / 'dist'
            
            @app.route('/')
            def index():
                return send_from_directory(frontend_dist, 'index.html')
            
            @app.route('/<path:path>')
            def serve_static(path):
                try:
                    return send_from_directory(frontend_dist, path)
                except (FileNotFoundError, OSError):
                    # Fallback to index.html for SPA routing
                    return send_from_directory(frontend_dist, 'index.html')
        
        except Exception as e:
            logger.error(f"Failed to register routes: {e}")
            # Fall back to basic routes
            @app.route('/')
            def index():
                return "AutoMetabuilder Server", 200
    
    return app


# Create the app instance for imports
flask_app = create_app()
# Wrap Flask app for ASGI compatibility (needed for uvicorn)
app = WsgiToAsgi(flask_app)
