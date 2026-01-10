from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .json_utils import read_json
from .metadata import load_metadata
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
    packages_name = metadata.get("workflow_packages_path", "workflow_packages")
    return PACKAGE_ROOT / packages_name


def load_workflow_packages() -> list[dict[str, Any]]:
    packages_dir = get_workflow_packages_dir()
    if not packages_dir.exists():
        return []
    packages: list[dict[str, Any]] = []
    for file in sorted(packages_dir.iterdir()):
        if file.suffix != ".json":
            continue
        data = read_json(file)
        if not isinstance(data, dict):
            continue
        pkg_id = data.get("id") or file.stem
        data["id"] = pkg_id
        data.setdefault("workflow", {"nodes": []})
        packages.append(data)
    return packages


def summarize_workflow_packages(packages: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for pkg in packages:
        summary.append(
            {
                "id": pkg["id"],
                "label": pkg.get("label") or pkg["id"],
                "description": pkg.get("description", ""),
                "tags": pkg.get("tags", []),
            }
        )
    return summary
