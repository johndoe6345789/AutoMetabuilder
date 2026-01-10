"""Workflow plugin: reset bot execution state."""
from autometabuilder.workflow.plugins.control.control_start_bot.control_start_bot import _reset_run_state


def run(_runtime, _inputs):
    """Reset bot execution state.
    
    Returns:
        Dictionary with:
            - reset: bool - Always True to indicate state was reset
    """
    _reset_run_state()
    return {"reset": True}
