"""Workflow plugin: get workflow content."""
from ....web.data.workflow import get_workflow_content


def run(_runtime, _inputs):
    """Get workflow content from workflow file."""
    content = get_workflow_content()
    return {"result": content}
