"""Load workflow packages from npm-style package directories."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List

from .json_utils import read_json

logger = logging.getLogger(__name__)


def load_package(package_dir: Path) -> Dict[str, Any] | None:
    """Load a single workflow package."""
    package_json = package_dir / "package.json"
    if not package_json.exists():
        logger.warning("Package %s missing package.json", package_dir.name)
        return None
    
    # Read package.json
    pkg_data = read_json(package_json)
    if not isinstance(pkg_data, dict):
        logger.warning("Invalid package.json in %s", package_dir.name)
        return None
    
    # Read workflow file
    workflow_file = pkg_data.get("main", "workflow.json")
    workflow_path = package_dir / workflow_file
    
    if not workflow_path.exists():
        logger.warning("Workflow file %s not found in %s", workflow_file, package_dir.name)
        return None
    
    workflow_data = read_json(workflow_path)
    if not isinstance(workflow_data, dict):
        logger.warning("Invalid workflow in %s", package_dir.name)
        return None
    
    # Combine package metadata with workflow
    metadata = pkg_data.get("metadata", {})
    
    return {
        "id": pkg_data.get("name", package_dir.name),
        "name": pkg_data.get("name", package_dir.name),
        "version": pkg_data.get("version", "1.0.0"),
        "description": pkg_data.get("description", ""),
        "author": pkg_data.get("author", ""),
        "license": pkg_data.get("license", ""),
        "keywords": pkg_data.get("keywords", []),
        "label": metadata.get("label", package_dir.name),
        "tags": metadata.get("tags", []),
        "icon": metadata.get("icon", "workflow"),
        "category": metadata.get("category", "templates"),
        "workflow": workflow_data,
    }


def load_all_packages(packages_dir: Path) -> List[Dict[str, Any]]:
    """Load all workflow packages from directory."""
    if not packages_dir.exists():
        logger.warning("Packages directory not found: %s", packages_dir)
        return []
    
    packages = []
    for item in sorted(packages_dir.iterdir()):
        if not item.is_dir():
            continue
        
        package = load_package(item)
        if package:
            packages.append(package)
    
    logger.debug("Loaded %d workflow packages", len(packages))
    return packages
