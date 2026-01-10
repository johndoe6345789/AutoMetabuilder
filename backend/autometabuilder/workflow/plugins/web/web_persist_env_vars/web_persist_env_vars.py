"""Workflow plugin: persist environment variables."""
from ....data.env import persist_env_vars


def run(_runtime, inputs):
    """Persist environment variables to .env file."""
    updates = inputs.get("updates", {})
    persist_env_vars(updates)
    return {"result": "Environment variables persisted"}
