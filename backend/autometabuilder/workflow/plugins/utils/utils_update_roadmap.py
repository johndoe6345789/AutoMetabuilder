"""Workflow plugin: update roadmap file."""
from ....roadmap_utils import update_roadmap


def run(_runtime, inputs):
    """Update ROADMAP.md with new content."""
    content = inputs.get("content")
    if not content:
        return {"error": "Content is required"}
    
    update_roadmap(content)
    return {"result": "ROADMAP.md updated successfully"}
