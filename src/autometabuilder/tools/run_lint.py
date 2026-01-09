"""Run pylint on a path."""
import logging
import subprocess

logger = logging.getLogger("autometabuilder")


def run_lint(path: str = "src") -> str:
    logger.info("Running linting in %s...", path)
    result = subprocess.run(["pylint", path], capture_output=True, text=True, check=False)
    logger.info(result.stdout)
    if result.stderr:
        logger.error(result.stderr)
    return result.stdout
