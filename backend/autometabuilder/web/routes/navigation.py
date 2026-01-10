"""Navigation and workflow metadata routes."""
from __future__ import annotations

from flask import Blueprint

from ..data import get_navigation_items, load_metadata, load_workflow_packages, summarize_workflow_packages
from ..workflow_graph import build_workflow_graph

navigation_bp = Blueprint("navigation", __name__)


@navigation_bp.route("/api/navigation")
def api_navigation() -> tuple[dict[str, object], int]:
    return {"items": get_navigation_items()}, 200


@navigation_bp.route("/api/workflow/packages")
def api_workflow_packages() -> tuple[dict[str, object], int]:
    packages = load_workflow_packages()
    return {"packages": summarize_workflow_packages(packages)}, 200


@navigation_bp.route("/api/workflow/packages/<package_id>")
def api_get_workflow_package(package_id: str) -> tuple[dict[str, object], int]:
    packages = load_workflow_packages()
    for pkg in packages:
        if pkg.get("id") == package_id:
            return pkg, 200
    return {"error": "package not found"}, 404


@navigation_bp.route("/api/workflow/plugins")
def api_workflow_plugins() -> tuple[dict[str, object], int]:
    return {"plugins": load_metadata().get("workflow_plugins", {})}, 200


@navigation_bp.route("/api/workflow/graph")
def api_workflow_graph() -> tuple[dict[str, object], int]:
    return build_workflow_graph(), 200
