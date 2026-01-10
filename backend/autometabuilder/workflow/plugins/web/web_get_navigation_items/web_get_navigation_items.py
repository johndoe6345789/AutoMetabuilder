"""Workflow plugin: get navigation items."""
import json
from pathlib import Path


def run(_runtime, _inputs):
    """Get navigation items."""
    # Path calculation
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    nav_path = package_root / "web" / "navigation_items.json"
    
    if not nav_path.exists():
        return {"result": []}
    
    try:
        nav = json.loads(nav_path.read_text(encoding="utf-8"))
        if isinstance(nav, list):
            return {"result": nav}
    except json.JSONDecodeError:
        pass
    
    return {"result": []}
