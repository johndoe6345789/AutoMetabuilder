"""Load metadata.json."""
import json
import os


def load_metadata() -> dict:
    metadata_path = os.path.join(os.path.dirname(__file__), "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)
