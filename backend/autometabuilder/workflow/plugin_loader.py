"""Load workflow plugins by dotted path."""
from ..loaders.callable_loader import load_callable


def load_plugin_callable(path: str):
    """Load a workflow plugin callable."""
    return load_callable(path)
