"""List files in the repo."""
import os
import logging

logger = logging.getLogger("autometabuilder")


def list_files(directory: str = ".") -> str:
    """Return newline-separated files under a directory."""
    files_list = []
    for root, _, files in os.walk(directory):
        if ".git" in root or "__pycache__" in root or ".venv" in root:
            continue
        for file in files:
            files_list.append(os.path.join(root, file))
    result = "\n".join(files_list)
    logger.info("Indexing repository files in %s...", directory)
    return result
