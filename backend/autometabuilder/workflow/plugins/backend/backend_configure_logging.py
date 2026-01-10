"""Workflow plugin: configure logging."""
import logging
import os

TRACE_LEVEL = 5


def _configure_logging() -> None:
    """Configure logging with TRACE support."""
    logging.addLevelName(TRACE_LEVEL, "TRACE")
    if not hasattr(logging, "TRACE"):
        setattr(logging, "TRACE", TRACE_LEVEL)

    def trace(self, message, *args, **kwargs):
        if self.isEnabledFor(TRACE_LEVEL):
            self.log(TRACE_LEVEL, message, *args, **kwargs)

    logging.Logger.trace = trace  # type: ignore[attr-defined]
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("autometabuilder.log"),
            logging.StreamHandler()
        ]
    )


def run(_runtime, _inputs):
    """
    Configure logging with TRACE support.
    
    Sets up logging with:
    - Custom TRACE level (level 5)
    - File and console handlers
    - Configurable log level from LOG_LEVEL env var
    
    Returns:
        dict: Success indicator
    """
    _configure_logging()
    return {"result": "Logging configured"}
