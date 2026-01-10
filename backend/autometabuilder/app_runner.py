"""Application runner."""
import logging
import os
from .utils import parse_args
from .loaders import load_env
from .utils.logging_config import configure_logging
from .loaders import load_metadata
from .web.server import start_web_ui
from .engine import load_workflow_config, build_workflow_context, build_workflow_engine


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
