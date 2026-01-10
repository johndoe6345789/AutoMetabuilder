"""Contract tests for AJAX endpoints used by the Next.js frontend."""
import pytest

from autometabuilder.data.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


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
