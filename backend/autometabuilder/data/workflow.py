from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .json_utils import read_json
from .metadata import load_metadata
from .package_loader import load_all_packages
from .paths import PACKAGE_ROOT


def get_workflow_content() -> str:
    metadata = load_metadata()
    workflow_name = metadata.get("workflow_path", "workflow.json")
    workflow_path = PACKAGE_ROOT / workflow_name
    if workflow_path.exists():
        return workflow_path.read_text(encoding="utf-8")
    return ""


def write_workflow(content: str) -> None:
    metadata = load_metadata()
    workflow_name = metadata.get("workflow_path", "workflow.json")
    workflow_path = PACKAGE_ROOT / workflow_name
    workflow_path.write_text(content or "", encoding="utf-8")


def get_workflow_packages_dir() -> Path:
    metadata = load_metadata()
    packages_name = metadata.get("workflow_packages_path", "packages")
    return PACKAGE_ROOT / packages_name


def load_workflow_packages() -> list[dict[str, Any]]:
    packages_dir = get_workflow_packages_dir()
    return load_all_packages(packages_dir)


def summarize_workflow_packages(packages: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for pkg in packages:
        summary.append(
            {
                "id": pkg["id"],
                "name": pkg.get("name", pkg["id"]),
                "label": pkg.get("label") or pkg["id"],
                "description": pkg.get("description", ""),
                "tags": pkg.get("tags", []),
                "version": pkg.get("version", "1.0.0"),
                "category": pkg.get("category", "templates"),
            }
        )
    return summary
