"""Workflow plugin: load workflow packages."""
import json
import logging
from pathlib import Path
from autometabuilder.utils import load_metadata

logger = logging.getLogger(__name__)


def run(_runtime, _inputs):
    """Load all workflow packages."""
    package_root = Path(__file__).resolve().parents[5]  # backend/autometabuilder
    metadata = load_metadata()
    packages_name = metadata.get("workflow_packages_path", "packages")
    packages_dir = package_root / packages_name
    
    if not packages_dir.exists():
        logger.warning("Packages directory not found: %s", packages_dir)
        return {"result": []}
    
    packages = []
    for item in sorted(packages_dir.iterdir()):
        if not item.is_dir():
            continue
        
        # Load package.json
        package_json = item / "package.json"
        if not package_json.exists():
            logger.warning("Package %s missing package.json", item.name)
            continue
        
        try:
            pkg_data = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Invalid package.json in %s", item.name)
            continue
        
        if not isinstance(pkg_data, dict):
            logger.warning("Invalid package.json in %s", item.name)
            continue
        
        # Read workflow file
        workflow_file = pkg_data.get("main", "workflow.json")
        workflow_path = item / workflow_file
        
        if not workflow_path.exists():
            logger.warning("Workflow file %s not found in %s", workflow_file, item.name)
            continue
        
        try:
            workflow_data = json.loads(workflow_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Invalid workflow in %s", item.name)
            continue
        
        if not isinstance(workflow_data, dict):
            logger.warning("Invalid workflow in %s", item.name)
            continue
        
        # Combine package metadata with workflow
        metadata_info = pkg_data.get("metadata", {})
        
        package = {
            "id": pkg_data.get("name", item.name),
            "name": pkg_data.get("name", item.name),
            "version": pkg_data.get("version", "1.0.0"),
            "description": pkg_data.get("description", ""),
            "author": pkg_data.get("author", ""),
            "license": pkg_data.get("license", ""),
            "keywords": pkg_data.get("keywords", []),
            "label": metadata_info.get("label", item.name),
            "tags": metadata_info.get("tags", []),
            "icon": metadata_info.get("icon", "workflow"),
            "category": metadata_info.get("category", "templates"),
            "workflow": workflow_data,
        }
        packages.append(package)
    
    logger.debug("Loaded %d workflow packages", len(packages))
    return {"result": packages}
