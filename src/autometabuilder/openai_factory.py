"""OpenAI client factory."""
import os
from openai import OpenAI

DEFAULT_ENDPOINT = "https://models.github.ai/inference"


def create_openai_client(token: str):
    return OpenAI(
        base_url=os.environ.get("GITHUB_MODELS_ENDPOINT", DEFAULT_ENDPOINT),
        api_key=token,
    )
