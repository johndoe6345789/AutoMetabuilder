"""Workflow plugin: load workflow packages."""
from ....data.workflow import load_workflow_packages


def run(_runtime, _inputs):
    """Load all workflow packages."""
    packages = load_workflow_packages()
    return {"result": packages}
