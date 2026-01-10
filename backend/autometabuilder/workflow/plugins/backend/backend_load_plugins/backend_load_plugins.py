"""Workflow plugin: load and register plugins."""
import importlib
import inspect
import logging
import os
from .....utils import get_package_root

logger = logging.getLogger("autometabuilder")


def _load_plugins(tool_map: dict, tools: list) -> None:
    """Load plugin tools and append metadata."""
    # Locate plugins directory in package root
    plugins_dir = get_package_root() / "plugins"
    if not os.path.exists(plugins_dir):
        return

    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f".plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name, package="autometabuilder")
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj) and hasattr(obj, "tool_metadata"):
                        tool_metadata = getattr(obj, "tool_metadata")
                        tool_map[name] = obj
                        tools.append(tool_metadata)
                        logger.info("Loaded plugin tool: %s", name)
            except Exception as error:  # pylint: disable=broad-exception-caught
                logger.error("Failed to load plugin %s: %s", filename, error)


def run(runtime, _inputs):
    """Load and register plugins."""
    tool_map = runtime.context.get("tool_map", {})
    tools = runtime.context.get("tools", [])
    _load_plugins(tool_map, tools)
    return {"result": True}
