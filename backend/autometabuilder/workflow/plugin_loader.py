"""Load workflow plugins by dotted path."""
import importlib


def load_plugin_callable(path: str):
    """Load a workflow plugin callable."""
    module_path, attr = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)
