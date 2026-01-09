"""Logging configuration with TRACE support."""
import logging
import os

TRACE_LEVEL = 5


def configure_logging() -> None:
    """Configure logging with TRACE support."""
    logging.addLevelName(TRACE_LEVEL, "TRACE")

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
