"""Run state helpers for long-lived bot executions."""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from typing import Dict

from ..roadmap_utils import is_mvp_reached

bot_process = None
mock_running = False
current_run_config: Dict[str, object] = {}


def _reset_run_state() -> None:
    global bot_process, current_run_config
    bot_process = None
    current_run_config = {}


def run_bot_task(mode: str, iterations: int, yolo: bool, stop_at_mvp: bool) -> None:
    global bot_process, mock_running, current_run_config
    current_run_config = {
        "mode": mode,
        "iterations": iterations,
        "yolo": yolo,
        "stop_at_mvp": stop_at_mvp,
    }

    if os.environ.get("MOCK_WEB_UI") == "true":
        mock_running = True
        time.sleep(5)
        mock_running = False
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
                bot_process = subprocess.Popen(cmd + ["--once"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                bot_process.wait()
        else:
            bot_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            bot_process.wait()
    finally:
        _reset_run_state()


def start_bot(mode: str = "once", iterations: int = 1, yolo: bool = True, stop_at_mvp: bool = False) -> bool:
    if bot_process is not None or mock_running:
        return False
    thread = threading.Thread(target=run_bot_task, args=(mode, iterations, yolo, stop_at_mvp), daemon=True)
    thread.start()
    return True
