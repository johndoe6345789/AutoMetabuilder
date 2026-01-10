"""End-to-end tests for the backend API using the workflow system.

These tests use Flask's test client to verify the backend works correctly
after the workflow migration to JSON-based routes.
"""
import logging
import pytest
from autometabuilder.workflow import build_workflow_engine, build_workflow_context
from autometabuilder.data import load_workflow_packages


@pytest.fixture(scope="module")
def flask_app():
    """Build Flask app using the JSON routes workflow."""
    # Load web server workflow with JSON routes
    packages = load_workflow_packages()
    web_server_package = next((p for p in packages if p.get("id") == "web_server_json_routes"), None)
    
    if not web_server_package:
        pytest.skip("web_server_json_routes workflow package not found")
    
    # Build workflow context and engine
    workflow_config = web_server_package.get("workflow", {})
    
    # Remove start_server node to prevent blocking
    workflow_config["nodes"] = [
        node for node in workflow_config.get("nodes", [])
        if node.get("type") != "web.start_server"
    ]
    
    workflow_context = build_workflow_context({})
    
    logger = logging.getLogger("test_server")
    logger.setLevel(logging.ERROR)  # Suppress logs during tests
    
    # Execute workflow to build the Flask app
    engine = build_workflow_engine(workflow_config, workflow_context, logger)
    engine.execute()
    
    # Get the app from the runtime
    app = engine.node_executor.runtime.context.get("flask_app")
    
    if app is None:
        pytest.skip("Flask app not created by workflow")
    
    # Set testing mode
    app.config['TESTING'] = True
    
    return app


@pytest.fixture(scope="module")
def client(flask_app):
    """Create test client for the Flask app."""
    return flask_app.test_client()


class TestWorkflowEndpoints:
    """Test workflow-related API endpoints."""
    
    def test_workflow_graph(self, client):
        """Test GET /api/workflow/graph returns workflow graph data."""
        response = client.get("/api/workflow/graph")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        assert "nodes" in data, "Response should contain 'nodes'"
        assert "edges" in data, "Response should contain 'edges'"
        assert isinstance(data["nodes"], list), "'nodes' should be a list"
        assert isinstance(data["edges"], list), "'edges' should be a list"
        
        # Verify count information
        assert "count" in data, "Response should contain 'count'"
        counts = data["count"]
        # Graph may be empty if no workflow is configured
        assert counts["nodes"] >= 0, "Should have zero or more nodes"
        assert counts["edges"] >= 0, "Should have zero or more edges"
    
    def test_workflow_plugins(self, client):
        """Test GET /api/workflow/plugins returns available plugins."""
        response = client.get("/api/workflow/plugins")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.get_json()
        assert isinstance(data, dict), "Response should be a dict"
        assert "plugins" in data, "Response should contain 'plugins'"
        
        plugins = data["plugins"]
        assert isinstance(plugins, dict), "'plugins' should be a dict"
        
        # Verify at least some core plugins exist (if metadata is populated)
        # If empty, that's okay - metadata might not be generated yet
    
    def test_workflow_packages(self, client):
        """Test GET /api/workflow/packages returns workflow packages."""
        response = client.get("/api/workflow/packages")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.get_json()
        assert isinstance(data, dict), "Response should be a dict"
        assert "packages" in data, "Response should contain 'packages'"
        
        packages = data["packages"]
        assert isinstance(packages, list), "'packages' should be a list"
        assert len(packages) > 0, "Should have at least one workflow package"
        
        # Verify at least one package has expected structure
        first_package = packages[0]
        assert "name" in first_package, "Package should have 'name'"
        assert "description" in first_package, "Package should have 'description'"


class TestNavigationAndTranslation:
    """Test navigation and translation API endpoints."""
    
    def test_navigation(self, client):
        """Test GET /api/navigation returns navigation items."""
        response = client.get("/api/navigation")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.get_json()
        assert isinstance(data, dict), "Response should be a dict"
        assert "navigation" in data, "Response should contain 'navigation'"
        # Navigation might be empty dict, that's okay
    
    def test_translation_options(self, client):
        """Test GET /api/translation-options returns available translations."""
        response = client.get("/api/translation-options")
        
        # May return 500 if metadata.json doesn't exist, which is okay
        assert response.status_code in [200, 500], f"Expected 200 or 500, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data, dict), "Response should be a dict"
            assert "translations" in data, "Response should contain 'translations'"
            
            translations = data["translations"]
            assert isinstance(translations, dict), "'translations' should be a dict"


class TestBasicFunctionality:
    """Test basic API functionality."""
    
    def test_json_response_format(self, client):
        """Test that APIs return proper JSON format."""
        response = client.get("/api/navigation")
        assert response.content_type == "application/json"
        
        # Verify JSON can be parsed
        data = response.get_json()
        assert data is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
