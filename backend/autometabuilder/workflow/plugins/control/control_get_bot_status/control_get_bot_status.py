"""Workflow plugin: get current bot execution status."""
from autometabuilder.workflow.plugins.control.control_start_bot.control_start_bot import (
    _bot_process,
    _mock_running,
    _current_run_config,
)


def run(_runtime, _inputs):
    """Get current bot execution status.
    
    Returns:
        Dictionary with:
            - is_running: bool - Whether the bot is currently running
            - config: dict - Current run configuration (empty if not running)
            - process: object - Bot process object (or None if not running)
    """
    return {
        "is_running": _bot_process is not None or _mock_running,
        "config": _current_run_config,
        "process": _bot_process,
    }
