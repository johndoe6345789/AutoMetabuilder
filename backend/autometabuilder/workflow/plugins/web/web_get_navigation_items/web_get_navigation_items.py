"""Workflow plugin: get navigation items."""
from ....data.navigation import get_navigation_items


def run(_runtime, _inputs):
    """Get navigation items."""
    items = get_navigation_items()
    return {"result": items}
