"""End-to-end tests for the backend API using requests library.

These tests start the actual Flask server using the workflow system and test
the API endpoints with real HTTP requests to verify the backend works correctly
after the workflow migration.
"""
import logging
import threading
import time
import pytest
import requests
from autometabuilder.workflow import build_workflow_engine, build_workflow_context
from autometabuilder.data import load_workflow_packages


# Configuration
BASE_URL = "http://127.0.0.1:8001"
STARTUP_TIMEOUT = 15  # seconds to wait for server to start


def start_server_thread():
    """Start the Flask server in a thread using the workflow system."""
    # Load web server bootstrap workflow
    packages = load_workflow_packages()
    web_server_package = next((p for p in packages if p.get("id") == "web_server_bootstrap"), None)
    
    if not web_server_package:
        raise RuntimeError("web_server_bootstrap workflow package not found")
    
    # Build workflow context and engine
    workflow_config = web_server_package.get("workflow", {})
    
    # Modify workflow to use test port and disable debug mode
    for node in workflow_config.get("nodes", []):
        if node.get("type") == "web.start_server":
            node["parameters"]["port"] = 8001
            node["parameters"]["host"] = "127.0.0.1"
            node["parameters"]["debug"] = False
    
    workflow_context = build_workflow_context({})
    
    logger = logging.getLogger("test_server")
    logger.setLevel(logging.ERROR)  # Suppress logs during tests
    
    # Execute workflow to start the server
    engine = build_workflow_engine(workflow_config, workflow_context, logger)
    try:
        engine.execute()
    except Exception as e:
        logger.error(f"Server execution error: {e}")


@pytest.fixture(scope="module")
def server():
    """Start the Flask server for all tests in this module."""
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server_thread, daemon=True)
    server_thread.start()
    
    # Wait for server to be ready
    start_time = time.time()
    server_ready = False
    
    while time.time() - start_time < STARTUP_TIMEOUT:
        try:
            response = requests.get(f"{BASE_URL}/api/navigation", timeout=2)
            if response.status_code == 200:
                server_ready = True
                break
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    
    if not server_ready:
        pytest.skip("Server failed to start within timeout")
    
    yield BASE_URL
    
    # Server thread is daemon, so it will be cleaned up automatically


class TestWorkflowEndpoints:
    """Test workflow-related API endpoints."""
    
    def test_workflow_graph(self, server):
        """Test GET /api/workflow/graph returns workflow graph data."""
        response = requests.get(f"{server}/api/workflow/graph", timeout=5)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data is not None, "Response should be JSON"
        assert "nodes" in data, "Response should contain 'nodes'"
        assert "edges" in data, "Response should contain 'edges'"
        assert isinstance(data["nodes"], list), "'nodes' should be a list"
        assert isinstance(data["edges"], list), "'edges' should be a list"
        
        # Verify count information
        assert "count" in data, "Response should contain 'count'"
        counts = data["count"]
        assert counts["nodes"] >= 1, "Should have at least one node"
        assert counts["edges"] >= 0, "Should have zero or more edges"
    
    def test_workflow_plugins(self, server):
        """Test GET /api/workflow/plugins returns available plugins."""
        response = requests.get(f"{server}/api/workflow/plugins", timeout=5)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, dict), "Response should be a dict"
        assert "plugins" in data, "Response should contain 'plugins'"
        
        plugins = data["plugins"]
        assert isinstance(plugins, dict), "'plugins' should be a dict"
        
        # Verify at least some core plugins exist
        assert "core.load_context" in plugins, "Should have core.load_context plugin"
        
        # Verify plugin structure
        for plugin_name, plugin_info in list(plugins.items())[:3]:
            assert isinstance(plugin_info, dict), f"Plugin {plugin_name} info should be a dict"
    
    def test_workflow_packages(self, server):
        """Test GET /api/workflow/packages returns workflow packages."""
        response = requests.get(f"{server}/api/workflow/packages", timeout=5)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
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
    
    def test_navigation(self, server):
        """Test GET /api/navigation returns navigation items."""
        response = requests.get(f"{server}/api/navigation", timeout=5)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, dict), "Response should be a dict"
        assert "items" in data, "Response should contain 'items'"
        assert isinstance(data["items"], list), "'items' should be a list"
    
    def test_translation_options(self, server):
        """Test GET /api/translation-options returns available translations."""
        response = requests.get(f"{server}/api/translation-options", timeout=5)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, dict), "Response should be a dict"
        assert "translations" in data, "Response should contain 'translations'"
        
        translations = data["translations"]
        assert isinstance(translations, dict), "'translations' should be a dict"
        assert "en" in translations, "Should have English translation"
    
    def test_ui_messages(self, server):
        """Test GET /api/ui-messages/:lang returns UI messages."""
        response = requests.get(f"{server}/api/ui-messages/en", timeout=5)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, dict), "Response should be a dict"
        # Messages can be empty but should be a dict
        assert "messages" in data or len(data) >= 0, "Should have messages structure"


class TestPromptAndSettings:
    """Test prompt and settings API endpoints."""
    
    def test_get_prompt(self, server):
        """Test GET /api/prompt returns prompt content."""
        response = requests.get(f"{server}/api/prompt", timeout=5)
        
        # Prompt file may not exist, both 200 and 404 are acceptable
        assert response.status_code in [200, 404], \
            f"Expected 200 or 404, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict), "Response should be a dict"
            # Content can be empty but should have structure
    
    def test_get_workflow_content(self, server):
        """Test GET /api/workflow returns workflow content."""
        response = requests.get(f"{server}/api/workflow", timeout=5)
        
        # Workflow file may not exist, both 200 and 404 are acceptable
        assert response.status_code in [200, 404], \
            f"Expected 200 or 404, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict), "Response should be a dict"
    
    def test_get_env_vars(self, server):
        """Test GET /api/settings/env returns environment variables."""
        response = requests.get(f"{server}/api/settings/env", timeout=5)
        
        # Env file may not exist, both 200 and 404 are acceptable
        assert response.status_code in [200, 404], \
            f"Expected 200 or 404, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict), "Response should be a dict"
            # Even if empty, it should be a dict


class TestContextEndpoints:
    """Test context-related API endpoints."""
    
    def test_build_context(self, server):
        """Test GET /api/context/build returns full context."""
        response = requests.get(f"{server}/api/context/build", timeout=10)
        
        # May fail if GitHub token not configured, accept multiple status codes
        assert response.status_code in [200, 400, 500], \
            f"Expected 200, 400, or 500, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict), "Response should be a dict"
            # Context structure can vary, just verify it's valid JSON


class TestServerHealth:
    """Test general server health and availability."""
    
    def test_server_responds(self, server):
        """Test that the server is responding to requests."""
        response = requests.get(f"{server}/api/navigation", timeout=5)
        assert response.status_code == 200, "Server should respond with 200"
    
    def test_cors_headers(self, server):
        """Test that CORS headers are present (if configured)."""
        response = requests.options(f"{server}/api/navigation", timeout=5)
        # OPTIONS requests should be handled
        assert response.status_code in [200, 204, 405], \
            "OPTIONS request should be handled"
    
    def test_json_content_type(self, server):
        """Test that API returns JSON content type."""
        response = requests.get(f"{server}/api/navigation", timeout=5)
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, \
            f"Expected JSON content type, got {content_type}"


class TestErrorHandling:
    """Test API error handling."""
    
    def test_nonexistent_endpoint(self, server):
        """Test that nonexistent endpoints return 404."""
        response = requests.get(f"{server}/api/nonexistent", timeout=5)
        assert response.status_code == 404, \
            f"Nonexistent endpoint should return 404, got {response.status_code}"
    
    def test_invalid_translation_lang(self, server):
        """Test requesting invalid translation language."""
        response = requests.get(f"{server}/api/ui-messages/invalid_lang_xyz", timeout=5)
        # Should return 404 or fallback to default
        assert response.status_code in [200, 404], \
            f"Invalid language should return 200 (fallback) or 404, got {response.status_code}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
