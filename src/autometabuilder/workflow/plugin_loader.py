"""Load workflow plugins by dotted path."""
from ..callable_loader import load_callable


def load_plugin_callable(path: str):
    return load_callable(path)
