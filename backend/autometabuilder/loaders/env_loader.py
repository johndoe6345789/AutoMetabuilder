"""Load environment variables from .env."""
from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables."""
    load_dotenv()
