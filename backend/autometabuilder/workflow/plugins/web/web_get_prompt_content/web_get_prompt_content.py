"""Workflow plugin: get prompt content."""
from ....data.prompt import get_prompt_content


def run(_runtime, _inputs):
    """Get prompt content from prompt file."""
    content = get_prompt_content()
    return {"result": content}
