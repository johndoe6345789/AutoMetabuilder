"""Workflow plugin: get recent logs."""
from pathlib import Path


def run(_runtime, inputs):
    """Get recent log entries."""
    lines = inputs.get("lines", 50)
    
    # Use hardcoded path logic from data/paths.py
    package_root = Path(__file__).resolve().parents[5]  # Go up to backend/autometabuilder
    repo_root = package_root.parent.parent
    log_file = repo_root / "autometabuilder.log"
    
    if not log_file.exists():
        return {"result": ""}
    
    with log_file.open("r", encoding="utf-8") as handle:
        content = handle.readlines()
    
    return {"result": "".join(content[-lines:])}
