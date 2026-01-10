"""Workflow plugin: write prompt."""
from ....web.data.prompt import write_prompt


def run(_runtime, inputs):
    """Write prompt content to file."""
    content = inputs.get("content", "")
    write_prompt(content)
    return {"result": "Prompt written successfully"}
