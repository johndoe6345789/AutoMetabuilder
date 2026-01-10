"""Workflow plugin: write workflow."""
from pathlib import Path
from autometabuilder.loaders.metadata_loader import load_metadata


def run(_runtime, inputs):
    """Write workflow content to file."""
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    content = inputs.get("content", "")
    metadata = load_metadata()
    workflow_name = metadata.get("workflow_path", "workflow.json")
    workflow_path = package_root / workflow_name
    workflow_path.write_text(content or "", encoding="utf-8")
    
    return {"result": "Workflow written successfully"}
