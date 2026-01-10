"""Workflow plugin: write workflow."""
from ....web.data.workflow import write_workflow


def run(_runtime, inputs):
    """Write workflow content to file."""
    content = inputs.get("content", "")
    write_workflow(content)
    return {"result": "Workflow written successfully"}
