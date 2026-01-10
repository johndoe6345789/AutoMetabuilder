"""Workflow plugin: start bot execution in background thread."""
import os
import subprocess
import sys
import threading
import time

from autometabuilder.roadmap_utils import is_mvp_reached

# Global state for bot process
_bot_process = None
_mock_running = False
_current_run_config = {}


def _reset_run_state() -> None:
    """Reset the bot run state."""
    global _bot_process, _current_run_config, _mock_running
    _bot_process = None
    _current_run_config = {}
    _mock_running = False


def get_bot_state():
    """Get the current bot state (public interface).
    
    Returns:
        dict: Bot state with keys: is_running, config, process
    """
    return {
        "is_running": _bot_process is not None or _mock_running,
        "config": _current_run_config,
        "process": _bot_process,
    }


def reset_bot_state():
    """Reset the bot state (public interface)."""
    _reset_run_state()


def _run_bot_task(mode: str, iterations: int, yolo: bool, stop_at_mvp: bool) -> None:
    """Execute bot task in background thread."""
    global _bot_process, _mock_running, _current_run_config
    _current_run_config = {
        "mode": mode,
        "iterations": iterations,
        "yolo": yolo,
        "stop_at_mvp": stop_at_mvp,
    }

    if os.environ.get("MOCK_WEB_UI") == "true":
        _mock_running = True
        time.sleep(5)
        _mock_running = False
        _reset_run_state()
        return

    try:
        cmd = [sys.executable, "-m", "autometabuilder.main"]
        if yolo:
            cmd.append("--yolo")
        if mode == "once":
            cmd.append("--once")
        if mode == "iterations" and iterations > 1:
            for _ in range(iterations):
                if stop_at_mvp and is_mvp_reached():
                    break
                _bot_process = subprocess.Popen(cmd + ["--once"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                _bot_process.wait()
        else:
            _bot_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            _bot_process.wait()
    finally:
        _reset_run_state()


def run(_runtime, inputs):
    """Start bot execution in background thread.
    
    Args:
        inputs: Dictionary with keys:
            - mode: str (default: "once") - Execution mode ("once", "iterations", etc.)
            - iterations: int (default: 1) - Number of iterations for "iterations" mode
            - yolo: bool (default: True) - Run in YOLO mode
            - stop_at_mvp: bool (default: False) - Stop when MVP is reached
    
    Returns:
        Dictionary with:
            - started: bool - Whether the bot was started successfully
            - error: str (optional) - Error message if bot is already running
    """
    global _bot_process, _mock_running
    
    mode = inputs.get("mode", "once")
    iterations = inputs.get("iterations", 1)
    yolo = inputs.get("yolo", True)
    stop_at_mvp = inputs.get("stop_at_mvp", False)
    
    # Check if bot is already running
    if _bot_process is not None or _mock_running:
        return {"started": False, "error": "Bot already running"}
    
    # Start bot in background thread
    thread = threading.Thread(
        target=_run_bot_task,
        args=(mode, iterations, yolo, stop_at_mvp),
        daemon=True
    )
    thread.start()
    
    return {"started": True}
