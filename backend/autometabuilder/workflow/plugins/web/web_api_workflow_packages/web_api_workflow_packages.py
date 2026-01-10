"""Workflow plugin: handle /api/workflow/packages endpoint."""


def run(_runtime, _inputs):
    """Return workflow packages."""
    from autometabuilder.data import load_workflow_packages, summarize_workflow_packages
    packages = load_workflow_packages()
    return {"result": {"packages": summarize_workflow_packages(packages)}}
