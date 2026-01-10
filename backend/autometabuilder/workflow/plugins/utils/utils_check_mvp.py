"""Workflow plugin: check if MVP is reached."""
from ....utils.roadmap_utils import is_mvp_reached


def run(_runtime, _inputs):
    """Check if the MVP section in ROADMAP.md is completed."""
    mvp_reached = is_mvp_reached()
    return {"mvp_reached": mvp_reached}
