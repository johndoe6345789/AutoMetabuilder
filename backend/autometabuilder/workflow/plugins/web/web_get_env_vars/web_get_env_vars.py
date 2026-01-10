"""Workflow plugin: get environment variables."""
from ....web.data.env import get_env_vars


def run(_runtime, _inputs):
    """Get environment variables from .env file."""
    env_vars = get_env_vars()
    return {"result": env_vars}
