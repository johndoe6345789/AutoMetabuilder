"""Workflow plugin registry."""
import json
import logging
import os
from .plugin_loader import load_plugin_callable

logger = logging.getLogger("autometabuilder")


def load_plugin_map() -> dict:
    """Load workflow plugin map JSON."""
    map_path = os.path.join(os.path.dirname(__file__), "plugin_map.json")
    if not os.path.exists(map_path):
        return {}
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        logger.error("Invalid workflow plugin map JSON.")
        return {}
    return data if isinstance(data, dict) else {}


class PluginRegistry:
    """Resolve workflow plugin handlers."""
    def __init__(self, plugin_map: dict):
        self._plugins = {}
        for node_type, path in plugin_map.items():
            try:
                self._plugins[node_type] = load_plugin_callable(path)
                logger.debug("Registered workflow plugin %s -> %s", node_type, path)
            except Exception as error:  # pylint: disable=broad-exception-caught
                logger.error("Failed to register plugin %s: %s", node_type, error)

    def get(self, node_type: str):
        """Return plugin handler for node type."""
        return self._plugins.get(node_type)
