"""Workflow plugin: parse CLI arguments."""
from ....utils.cli_args import parse_args


def run(runtime, _inputs):
    """Parse command line arguments."""
    args = parse_args()
    # Store in context for other plugins
    runtime.context["args"] = args
    return {
        "dry_run": args.dry_run,
        "yolo": args.yolo,
        "once": args.once,
        "web": args.web
    }
