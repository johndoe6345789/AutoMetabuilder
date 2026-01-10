"""Workflow plugin: get current bot execution status."""
from autometabuilder.workflow.plugins.control.control_start_bot.control_start_bot import get_bot_state


def run(_runtime, _inputs):
    """Get current bot execution status.
    
    Returns:
        Dictionary with:
            - is_running: bool - Whether the bot is currently running
            - config: dict - Current run configuration (empty if not running)
            - process: object - Bot process object (or None if not running)
    """
    return get_bot_state()
