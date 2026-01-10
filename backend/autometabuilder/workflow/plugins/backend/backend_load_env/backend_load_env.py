"""Workflow plugin: load environment variables."""
from dotenv import load_dotenv


def run(_runtime, _inputs):
    """Load environment variables from .env file."""
    load_dotenv()
    return {"result": "Environment loaded"}
