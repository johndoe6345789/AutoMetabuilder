"""Workflow plugin: load environment variables."""
from ....loaders.env_loader import load_env


def run(_runtime, _inputs):
    """Load environment variables from .env file."""
    load_env()
    return {"result": "Environment loaded"}
