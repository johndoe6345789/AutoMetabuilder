"""Workflow plugin: parse CLI arguments."""
import argparse


def _parse_args():
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


def run(runtime, _inputs):
    """Parse command line arguments."""
    args = _parse_args()
    # Store in context for other plugins
    runtime.context["args"] = args
    return {
        "dry_run": args.dry_run,
        "yolo": args.yolo,
        "once": args.once,
        "web": args.web
    }
