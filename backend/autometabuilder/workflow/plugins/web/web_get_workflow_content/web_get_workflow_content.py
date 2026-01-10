"""Workflow plugin: get workflow content."""
from pathlib import Path
from autometabuilder.loaders.metadata_loader import load_metadata


def run(_runtime, _inputs):
    """Get workflow content from workflow file."""
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    metadata = load_metadata()
    workflow_name = metadata.get("workflow_path", "workflow.json")
    workflow_path = package_root / workflow_name
    
    if workflow_path.exists():
        content = workflow_path.read_text(encoding="utf-8")
        return {"result": content}
    
    return {"result": ""}
