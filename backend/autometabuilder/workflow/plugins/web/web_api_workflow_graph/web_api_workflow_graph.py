"""Workflow plugin: handle /api/workflow/graph endpoint."""


def run(_runtime, _inputs):
    """Return workflow graph."""
    from autometabuilder.workflow.workflow_graph import build_workflow_graph
    graph = build_workflow_graph()
    return {"result": graph}
