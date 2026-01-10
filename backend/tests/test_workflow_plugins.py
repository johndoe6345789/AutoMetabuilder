"""Test new workflow plugins for software development primitives."""
from autometabuilder.workflow.plugin_registry import PluginRegistry, load_plugin_map
from autometabuilder.workflow.runtime import WorkflowRuntime
import logging


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


def test_plugin_map_loads_all_new_plugins():
    """Test that plugin map includes all new plugins."""
    plugin_map = load_plugin_map()
    
    # Test logic plugins
    assert "logic.and" in plugin_map
    assert "logic.or" in plugin_map
    assert "logic.xor" in plugin_map
    assert "logic.equals" in plugin_map
    assert "logic.gt" in plugin_map
    assert "logic.lt" in plugin_map
    
    # Test list plugins
    assert "list.find" in plugin_map
    assert "list.some" in plugin_map
    assert "list.every" in plugin_map
    assert "list.concat" in plugin_map
    assert "list.slice" in plugin_map
    assert "list.sort" in plugin_map
    assert "list.length" in plugin_map
    
    # Test dict plugins
    assert "dict.get" in plugin_map
    assert "dict.set" in plugin_map
    assert "dict.merge" in plugin_map
    
    # Test string plugins
    assert "string.concat" in plugin_map
    assert "string.split" in plugin_map
    assert "string.upper" in plugin_map
    assert "string.lower" in plugin_map
    
    # Test math plugins
    assert "math.add" in plugin_map
    assert "math.subtract" in plugin_map
    assert "math.multiply" in plugin_map
    assert "math.divide" in plugin_map
    
    # Test conversion plugins
    assert "convert.to_string" in plugin_map
    assert "convert.to_number" in plugin_map
    assert "convert.parse_json" in plugin_map
    assert "convert.to_json" in plugin_map
    
    # Test control flow plugins
    assert "control.switch" in plugin_map
    
    # Test variable plugins
    assert "var.get" in plugin_map
    assert "var.set" in plugin_map
    
    # Test backend plugins
    assert "backend.load_metadata" in plugin_map
    assert "backend.load_messages" in plugin_map


def test_logic_and_plugin():
    """Test logic.and plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("logic.and")
    assert plugin is not None
    
    result = plugin(runtime, {"values": [True, True, True]})
    assert result["result"] is True
    
    result = plugin(runtime, {"values": [True, False, True]})
    assert result["result"] is False


def test_logic_or_plugin():
    """Test logic.or plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("logic.or")
    assert plugin is not None
    
    result = plugin(runtime, {"values": [False, False, True]})
    assert result["result"] is True
    
    result = plugin(runtime, {"values": [False, False, False]})
    assert result["result"] is False


def test_logic_equals_plugin():
    """Test logic.equals plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("logic.equals")
    assert plugin is not None
    
    result = plugin(runtime, {"a": 5, "b": 5})
    assert result["result"] is True
    
    result = plugin(runtime, {"a": 5, "b": 10})
    assert result["result"] is False


def test_math_add_plugin():
    """Test math.add plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("math.add")
    assert plugin is not None
    
    result = plugin(runtime, {"numbers": [1, 2, 3, 4, 5]})
    assert result["result"] == 15


def test_math_multiply_plugin():
    """Test math.multiply plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("math.multiply")
    assert plugin is not None
    
    result = plugin(runtime, {"numbers": [2, 3, 4]})
    assert result["result"] == 24


def test_string_concat_plugin():
    """Test string.concat plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("string.concat")
    assert plugin is not None
    
    result = plugin(runtime, {"strings": ["Hello", "World"], "separator": " "})
    assert result["result"] == "Hello World"


def test_string_upper_plugin():
    """Test string.upper plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("string.upper")
    assert plugin is not None
    
    result = plugin(runtime, {"text": "hello"})
    assert result["result"] == "HELLO"


def test_list_length_plugin():
    """Test list.length plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("list.length")
    assert plugin is not None
    
    result = plugin(runtime, {"items": [1, 2, 3, 4, 5]})
    assert result["result"] == 5


def test_list_concat_plugin():
    """Test list.concat plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("list.concat")
    assert plugin is not None
    
    result = plugin(runtime, {"lists": [[1, 2], [3, 4], [5, 6]]})
    assert result["result"] == [1, 2, 3, 4, 5, 6]


def test_dict_get_plugin():
    """Test dict.get plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("dict.get")
    assert plugin is not None
    
    result = plugin(runtime, {"object": {"name": "John", "age": 30}, "key": "name"})
    assert result["result"] == "John"
    assert result["found"] is True
    
    result = plugin(runtime, {"object": {"name": "John"}, "key": "missing", "default": "N/A"})
    assert result["result"] == "N/A"
    assert result["found"] is False


def test_dict_set_plugin():
    """Test dict.set plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("dict.set")
    assert plugin is not None
    
    result = plugin(runtime, {"object": {"a": 1}, "key": "b", "value": 2})
    assert result["result"] == {"a": 1, "b": 2}


def test_var_get_set_plugin():
    """Test var.get and var.set plugins."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    set_plugin = registry.get("var.set")
    get_plugin = registry.get("var.get")
    
    assert set_plugin is not None
    assert get_plugin is not None
    
    # Set a variable
    set_result = set_plugin(runtime, {"key": "test_var", "value": 42})
    assert set_result["result"] == 42
    
    # Get the variable
    get_result = get_plugin(runtime, {"key": "test_var"})
    assert get_result["result"] == 42
    assert get_result["exists"] is True


def test_convert_to_json_and_parse():
    """Test JSON conversion plugins."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    to_json = registry.get("convert.to_json")
    parse_json = registry.get("convert.parse_json")
    
    assert to_json is not None
    assert parse_json is not None
    
    # Convert to JSON
    data = {"name": "Test", "value": 123}
    json_result = to_json(runtime, {"value": data})
    json_str = json_result["result"]
    
    # Parse JSON back
    parse_result = parse_json(runtime, {"text": json_str})
    assert parse_result["result"] == data


def test_convert_to_number():
    """Test number conversion."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("convert.to_number")
    assert plugin is not None
    
    result = plugin(runtime, {"value": "42"})
    assert result["result"] == 42
    
    result = plugin(runtime, {"value": "3.14"})
    assert result["result"] == 3.14


def test_control_switch():
    """Test control.switch plugin."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = create_test_runtime()
    
    plugin = registry.get("control.switch")
    assert plugin is not None
    
    cases = {
        "option1": "Result 1",
        "option2": "Result 2",
        "option3": "Result 3"
    }
    
    result = plugin(runtime, {"value": "option2", "cases": cases})
    assert result["result"] == "Result 2"
    assert result["matched"] is True
    
    result = plugin(runtime, {"value": "unknown", "cases": cases, "default": "Default"})
    assert result["result"] == "Default"
    assert result["matched"] is False
