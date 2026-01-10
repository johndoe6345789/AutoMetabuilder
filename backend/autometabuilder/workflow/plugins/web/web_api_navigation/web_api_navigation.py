"""Workflow plugin: handle /api/navigation endpoint."""


def run(_runtime, _inputs):
    """Return navigation items."""
    from autometabuilder.data import get_navigation_items
    return {"result": {"navigation": get_navigation_items()}}
