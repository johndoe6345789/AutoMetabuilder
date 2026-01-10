"""Test the new unit testing workflow plugins."""
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


def test_assert_equals_pass():
    """Test test.assert_equals plugin when values are equal."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_equals")
    assert plugin is not None
    
    result = plugin(runtime, {"actual": 42, "expected": 42})
    assert result["passed"] is True
    assert result["actual"] == 42
    assert result["expected"] == 42


def test_assert_equals_fail():
    """Test test.assert_equals plugin when values are not equal."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_equals")
    assert plugin is not None
    
    result = plugin(runtime, {"actual": 42, "expected": 24, "message": "Test message"})
    assert result["passed"] is False
    assert "error" in result
    assert "Test message" in result["error"]


def test_assert_true_pass():
    """Test test.assert_true plugin when value is true."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_true")
    assert plugin is not None
    
    result = plugin(runtime, {"value": True})
    assert result["passed"] is True


def test_assert_true_fail():
    """Test test.assert_true plugin when value is not true."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_true")
    assert plugin is not None
    
    result = plugin(runtime, {"value": False})
    assert result["passed"] is False
    assert "error" in result


def test_assert_false_pass():
    """Test test.assert_false plugin when value is false."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_false")
    assert plugin is not None
    
    result = plugin(runtime, {"value": False})
    assert result["passed"] is True


def test_assert_false_fail():
    """Test test.assert_false plugin when value is not false."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_false")
    assert plugin is not None
    
    result = plugin(runtime, {"value": True})
    assert result["passed"] is False
    assert "error" in result


def test_assert_exists_pass():
    """Test test.assert_exists plugin when value exists."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_exists")
    assert plugin is not None
    
    result = plugin(runtime, {"value": "some value"})
    assert result["passed"] is True


def test_assert_exists_fail():
    """Test test.assert_exists plugin when value is None."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.assert_exists")
    assert plugin is not None
    
    result = plugin(runtime, {"value": None})
    assert result["passed"] is False
    assert "error" in result


def test_run_suite_all_pass():
    """Test test.run_suite plugin when all tests pass."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.run_suite")
    assert plugin is not None
    
    results = [
        {"passed": True},
        {"passed": True},
        {"passed": True}
    ]
    
    result = plugin(runtime, {"results": results, "suite_name": "Test Suite"})
    assert result["passed"] is True
    assert result["total"] == 3
    assert result["passed_count"] == 3
    assert result["failed_count"] == 0
    assert len(result["failures"]) == 0


def test_run_suite_with_failures():
    """Test test.run_suite plugin when some tests fail."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("test.run_suite")
    assert plugin is not None
    
    results = [
        {"passed": True},
        {"passed": False, "error": "Test failed", "expected": 5, "actual": 3},
        {"passed": True}
    ]
    
    result = plugin(runtime, {"results": results})
    assert result["passed"] is False
    assert result["total"] == 3
    assert result["passed_count"] == 2
    assert result["failed_count"] == 1
    assert len(result["failures"]) == 1
    assert result["failures"][0]["test_index"] == 1
    assert "Test failed" in result["failures"][0]["error"]


def test_var_plugins():
    """Test var.get, var.set, var.exists, var.delete plugins."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    set_plugin = registry.get("var.set")
    get_plugin = registry.get("var.get")
    exists_plugin = registry.get("var.exists")
    delete_plugin = registry.get("var.delete")
    
    assert set_plugin is not None
    assert get_plugin is not None
    assert exists_plugin is not None
    assert delete_plugin is not None
    
    # Set a variable
    set_result = set_plugin(runtime, {"key": "test_key", "value": "test_value"})
    assert set_result["result"] == "test_value"
    assert set_result["key"] == "test_key"
    
    # Check if exists
    exists_result = exists_plugin(runtime, {"key": "test_key"})
    assert exists_result["result"] is True
    
    # Get the variable
    get_result = get_plugin(runtime, {"key": "test_key"})
    assert get_result["result"] == "test_value"
    assert get_result["exists"] is True
    
    # Delete the variable
    delete_result = delete_plugin(runtime, {"key": "test_key"})
    assert delete_result["result"] is True
    assert delete_result["deleted"] is True
    
    # Check if still exists
    exists_result2 = exists_plugin(runtime, {"key": "test_key"})
    assert exists_result2["result"] is False
    
    # Try to get deleted variable
    get_result2 = get_plugin(runtime, {"key": "test_key", "default": "default_value"})
    assert get_result2["result"] == "default_value"
    assert get_result2["exists"] is False
