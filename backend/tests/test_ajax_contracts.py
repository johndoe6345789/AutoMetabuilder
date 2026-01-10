"""Contract tests for AJAX endpoints used by the Next.js frontend."""
import pytest
import logging
from autometabuilder.workflow import build_workflow_engine, build_workflow_context
from autometabuilder.data import load_workflow_packages


@pytest.fixture
def client():
    """Build Flask app using workflow and return test client."""
    # Load web server bootstrap workflow
    packages = load_workflow_packages()
    web_server_package = next((p for p in packages if p.get("id") == "web_server_bootstrap"), None)
    
    if not web_server_package:
        pytest.skip("web_server_bootstrap workflow package not found")
    
    # Build workflow context and engine
    workflow_config = web_server_package.get("workflow", {})
    
    # Remove the start_server node to prevent blocking
    workflow_config["nodes"] = [
        node for node in workflow_config.get("nodes", [])
        if node.get("type") != "web.start_server"
    ]
    
    # Remove connections to start_server
    connections = workflow_config.get("connections", {})
    for node_name, node_connections in connections.items():
        for conn_type, conn_list in node_connections.items():
            if isinstance(conn_list, dict):
                for idx, targets in conn_list.items():
                    if isinstance(targets, list):
                        conn_list[idx] = [
                            t for t in targets
                            if t.get("node") != "Start Web Server"
                        ]
    
    workflow_context = build_workflow_context({})
    
    logger = logging.getLogger("test")
    logger.setLevel(logging.ERROR)  # Suppress logs during tests
    
    # Execute workflow to build the Flask app (but not start the server)
    engine = build_workflow_engine(workflow_config, workflow_context, logger)
    
    # Get the Flask app from the workflow execution
    # The workflow stores the app in the runtime context
    engine.execute()
    
    # Get the app from the runtime
    app = engine.node_executor.runtime.context.get("flask_app")
    
    if app is None:
        pytest.skip("Flask app not created by workflow")
    
    with app.test_client() as test_client:
        yield test_client


def test_workflow_graph_contract(client):
    response = client.get("/api/workflow/graph")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload is not None, "workflow graph response should be JSON"
    assert isinstance(payload.get("nodes"), list)
    assert isinstance(payload.get("edges"), list)
    counts = payload.get("count", {})
    assert counts.get("nodes", 0) >= 1
    assert counts.get("edges", 0) >= 0


def test_workflow_plugins_contract(client):
    response = client.get("/api/workflow/plugins")
    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, dict)
    plugins = payload.get("plugins", {})
    assert isinstance(plugins, dict)
    assert "core.load_context" in plugins


def test_navigation_and_translation_contract(client):
    nav_response = client.get("/api/navigation")
    assert nav_response.status_code == 200
    nav_payload = nav_response.get_json()
    assert isinstance(nav_payload, dict)
    assert isinstance(nav_payload.get("items"), list)
    trans_response = client.get("/api/translation-options")
    assert trans_response.status_code == 200
    trans_payload = trans_response.get_json()
    assert isinstance(trans_payload, dict)
    translations = trans_payload.get("translations", {})
    assert "en" in translations
