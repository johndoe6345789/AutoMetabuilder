"""Tests for web workflow plugins."""
import os
import tempfile
from pathlib import Path
from autometabuilder.workflow.plugin_registry import PluginRegistry, load_plugin_map
from autometabuilder.workflow.runtime import WorkflowRuntime


class MockLogger:
    """Mock logger for testing."""
    def info(self, *args, **kwargs):
        pass
    
    def debug(self, *args, **kwargs):
        pass
    
    def error(self, *args, **kwargs):
        pass


def create_test_runtime():
    """Create a test runtime with empty context."""
    logger = MockLogger()
    return WorkflowRuntime(context={}, store={}, tool_runner=None, logger=logger)


def test_plugin_map_includes_web_plugins():
    """Test that plugin map includes all new web plugins."""
    plugin_map = load_plugin_map()
    
    # Test web data plugins
    assert "web.get_env_vars" in plugin_map
    assert "web.persist_env_vars" in plugin_map
    assert "web.get_recent_logs" in plugin_map
    assert "web.read_json" in plugin_map
    assert "web.load_messages" in plugin_map
    assert "web.write_messages_dir" in plugin_map
    assert "web.get_navigation_items" in plugin_map
    assert "web.get_prompt_content" in plugin_map
    assert "web.write_prompt" in plugin_map
    assert "web.build_prompt_yaml" in plugin_map
    assert "web.get_workflow_content" in plugin_map
    assert "web.write_workflow" in plugin_map
    assert "web.load_workflow_packages" in plugin_map
    assert "web.summarize_workflow_packages" in plugin_map
    
    # Test translation plugins
    assert "web.load_translation" in plugin_map
    assert "web.list_translations" in plugin_map
    assert "web.create_translation" in plugin_map
    assert "web.update_translation" in plugin_map
    assert "web.delete_translation" in plugin_map
    assert "web.get_ui_messages" in plugin_map
    
    # Test Flask/server plugins
    assert "web.create_flask_app" in plugin_map
    assert "web.register_blueprint" in plugin_map
    assert "web.start_server" in plugin_map
    assert "web.build_context" in plugin_map


def test_web_read_json_plugin():
    """Test web.read_json plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.read_json")
    assert plugin is not None
    
    # Test with non-existent file (should return empty dict)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"test": "value"}')
        temp_path = f.name
    
    try:
        result = plugin(runtime, {"path": temp_path})
        assert "result" in result
        assert result["result"]["test"] == "value"
    finally:
        os.unlink(temp_path)


def test_web_build_prompt_yaml_plugin():
    """Test web.build_prompt_yaml plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.build_prompt_yaml")
    assert plugin is not None
    
    result = plugin(runtime, {
        "system_content": "You are a helpful assistant",
        "user_content": "Help me with coding",
        "model": "openai/gpt-4o"
    })
    
    assert "result" in result
    yaml_content = result["result"]
    assert "messages:" in yaml_content
    assert "role: system" in yaml_content
    assert "role: user" in yaml_content
    assert "model: openai/gpt-4o" in yaml_content


def test_web_create_flask_app_plugin():
    """Test web.create_flask_app plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.create_flask_app")
    assert plugin is not None
    
    result = plugin(runtime, {
        "name": "test_app",
        "config": {"JSON_SORT_KEYS": False}
    })
    
    assert "result" in result
    assert runtime.context.get("flask_app") is not None
    
    app = runtime.context["flask_app"]
    assert app.config["JSON_SORT_KEYS"] is False


def test_web_register_blueprint_plugin():
    """Test web.register_blueprint plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    # First create a Flask app
    create_app_plugin = registry.get("web.create_flask_app")
    create_app_plugin(runtime, {"name": "test_app"})
    
    # Now test registering a blueprint
    plugin = registry.get("web.register_blueprint")
    assert plugin is not None
    
    result = plugin(runtime, {
        "blueprint_path": "autometabuilder.web.routes.context.context_bp"
    })
    
    assert "result" in result
    assert "registered" in result["result"]


def test_web_get_ui_messages_plugin():
    """Test web.get_ui_messages plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.get_ui_messages")
    assert plugin is not None
    
    result = plugin(runtime, {"lang": "en"})
    
    assert "result" in result
    assert isinstance(result["result"], dict)
    assert result["result"].get("__lang") == "en"


def test_web_list_translations_plugin():
    """Test web.list_translations plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.list_translations")
    assert plugin is not None
    
    result = plugin(runtime, {})
    
    assert "result" in result
    assert isinstance(result["result"], dict)


def test_web_load_workflow_packages_plugin():
    """Test web.load_workflow_packages plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.load_workflow_packages")
    assert plugin is not None
    
    result = plugin(runtime, {})
    
    assert "result" in result
    assert isinstance(result["result"], list)


def test_web_summarize_workflow_packages_plugin():
    """Test web.summarize_workflow_packages plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.summarize_workflow_packages")
    assert plugin is not None
    
    packages = [
        {
            "id": "test_pkg",
            "name": "Test Package",
            "description": "A test package",
            "version": "1.0.0"
        }
    ]
    
    result = plugin(runtime, {"packages": packages})
    
    assert "result" in result
    assert isinstance(result["result"], list)
    assert len(result["result"]) == 1
    assert result["result"][0]["id"] == "test_pkg"


def test_web_build_context_plugin():
    """Test web.build_context plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("web.build_context")
    assert plugin is not None
    
    result = plugin(runtime, {})
    
    assert "result" in result
    context = result["result"]
    
    # Verify expected keys in context
    assert "logs" in context
    assert "env_vars" in context
    assert "translations" in context
    assert "metadata" in context
    assert "navigation" in context
    assert "status" in context
