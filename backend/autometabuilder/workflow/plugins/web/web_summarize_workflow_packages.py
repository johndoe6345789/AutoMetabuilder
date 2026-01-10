"""Workflow plugin: summarize workflow packages."""
from ....web.data.workflow import summarize_workflow_packages


def run(_runtime, inputs):
    """Summarize workflow packages."""
    packages = inputs.get("packages", [])
    summary = summarize_workflow_packages(packages)
    return {"result": summary}
