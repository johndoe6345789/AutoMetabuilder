def hello_plugin():
    """A simple plugin that returns a greeting."""
    return "Hello from the plugin system!"

hello_plugin.tool_metadata = {
    "type": "function",
    "function": {
        "name": "hello_plugin",
        "description": "A simple greeting from the plugin system.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}
