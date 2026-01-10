"""Load a callable by dotted path."""
import importlib


def load_callable(path: str):
    """Import and return a callable."""
    module_path, attr = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)
