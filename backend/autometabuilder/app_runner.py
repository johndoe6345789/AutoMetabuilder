"""Application runner."""
import argparse
import logging
import os
from .loaders import load_env
from .loaders import load_metadata
from .web.server import start_web_ui
from .engine import load_workflow_config, build_workflow_context, build_workflow_engine

TRACE_LEVEL = 5


def configure_logging() -> None:
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


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="AutoMetabuilder: AI-driven SDLC assistant.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not execute state-modifying tools."
    )
    parser.add_argument(
        "--yolo",
        action="store_true",
        help="Execute tools without confirmation."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single full iteration (AI -> Tool -> AI)."
    )
    parser.add_argument("--web", action="store_true", help="Start the Web UI.")
    return parser.parse_args()


def run_app() -> None:
    """Run the AutoMetabuilder CLI."""
    load_env()
    configure_logging()
    logger = logging.getLogger("autometabuilder")

    args = parse_args()
    if args.web:
        logger.info("Starting Web UI...")
        start_web_ui()
        return

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.error("GITHUB_TOKEN environment variable is required")
        return

    # Build minimal workflow context - workflow plugins handle initialization
    context_parts = {
        "args": args,
        "github_token": token
    }
    workflow_context = build_workflow_context(context_parts)
    
    metadata = load_metadata()
    workflow_config = load_workflow_config(metadata)
    
    logger.info("Starting workflow: %s", workflow_config.get("name", "Unnamed"))
    engine = build_workflow_engine(workflow_config, workflow_context, logger)
    engine.execute()
