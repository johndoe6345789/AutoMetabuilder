"""Run pytest on a path."""
import logging
import subprocess

logger = logging.getLogger("autometabuilder")


def run_tests(path: str = "tests") -> str:
    logger.info("Running tests in %s...", path)
    result = subprocess.run(["pytest", path], capture_output=True, text=True, check=False)
    logger.info(result.stdout)
    if result.stderr:
        logger.error(result.stderr)
    return result.stdout
