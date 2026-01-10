"""Data access layer that delegates to workflow plugins.

This module provides a simple API for data access by wrapping workflow plugins.
Routes and other code can import from here to access data functions.
"""

from autometabuilder.workflow.plugin_registry import PluginRegistry, load_plugin_map
from autometabuilder.workflow.runtime import WorkflowRuntime
import logging

# Create a minimal runtime for plugin execution
_logger = logging.getLogger(__name__)


class _SimpleLogger:
    """Minimal logger for plugin execution."""
    def info(self, *args, **kwargs):
        _logger.info(*args, **kwargs)
    
    def debug(self, *args, **kwargs):
        _logger.debug(*args, **kwargs)
    
    def error(self, *args, **kwargs):
        _logger.error(*args, **kwargs)


def _run_plugin(plugin_name, inputs=None):
    """Execute a workflow plugin and return its result."""
    plugin_map = load_plugin_map()
    registry = PluginRegistry(plugin_map)
    runtime = WorkflowRuntime(
        context={},
        store={},
        tool_runner=None,
        logger=_SimpleLogger()
    )
    
    plugin = registry.get(plugin_name)
    if not plugin:
        raise RuntimeError(f"Plugin {plugin_name} not found")
    
    result = plugin(runtime, inputs or {})
    return result.get("result")


# Environment functions
def get_env_vars():
    """Get environment variables from .env file."""
    return _run_plugin("web.get_env_vars")


def persist_env_vars(updates):
    """Persist environment variables to .env file."""
    return _run_plugin("web.persist_env_vars", {"updates": updates})


# Log functions
def get_recent_logs(lines=50):
    """Get recent log entries."""
    return _run_plugin("web.get_recent_logs", {"lines": lines})


# Navigation functions
def get_navigation_items():
    """Get navigation menu items."""
    return _run_plugin("web.get_navigation_items")


# Prompt functions
def get_prompt_content():
    """Get prompt content from prompt file."""
    return _run_plugin("web.get_prompt_content")


def write_prompt(content):
    """Write prompt content to file."""
    return _run_plugin("web.write_prompt", {"content": content})


def build_prompt_yaml(system_content, user_content, model):
    """Build prompt YAML from components."""
    return _run_plugin("web.build_prompt_yaml", {
        "system_content": system_content,
        "user_content": user_content,
        "model": model
    })


# Workflow functions
def get_workflow_content():
    """Get workflow content from workflow file."""
    return _run_plugin("web.get_workflow_content")


def write_workflow(content):
    """Write workflow content to file."""
    return _run_plugin("web.write_workflow", {"content": content})


def load_workflow_packages():
    """Load all workflow packages."""
    return _run_plugin("web.load_workflow_packages")


def summarize_workflow_packages(packages):
    """Summarize workflow packages."""
    return _run_plugin("web.summarize_workflow_packages", {"packages": packages})


# Translation functions
def list_translations():
    """List all available translations."""
    return _run_plugin("web.list_translations")


def load_translation(lang):
    """Load translation for a specific language."""
    return _run_plugin("web.load_translation", {"lang": lang})


def create_translation(lang):
    """Create a new translation."""
    return _run_plugin("web.create_translation", {"lang": lang})


def update_translation(lang, payload):
    """Update an existing translation."""
    return _run_plugin("web.update_translation", {"lang": lang, "payload": payload})


def delete_translation(lang):
    """Delete a translation."""
    return _run_plugin("web.delete_translation", {"lang": lang})


def get_ui_messages(lang):
    """Get UI messages for a specific language with fallback."""
    return _run_plugin("web.get_ui_messages", {"lang": lang})


# Metadata - still using loaders directly
from autometabuilder.loaders.metadata_loader import load_metadata
