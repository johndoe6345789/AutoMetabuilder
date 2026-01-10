"""Build a node/edge view of the declarative workflow for visualization."""
from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List

from .data import get_workflow_content, load_metadata


def _parse_workflow_definition() -> Dict[str, Any]:
    payload = get_workflow_content()
    if not payload:
        return {"nodes": []}
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return {"nodes": []}
    return parsed if isinstance(parsed, dict) else {"nodes": []}


def _gather_nodes(nodes: Iterable[Dict[str, Any]], plugin_map: Dict[str, Any], parent_id: str | None = None, collected: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    collected = collected or []
    for node in nodes:
        node_id = node.get("id") or f"node-{len(collected)}"
        node_type = node.get("type", "unknown")
        metadata = plugin_map.get(node_type, {})
        node_summary: Dict[str, Any] = {
            "id": node_id,
            "type": node_type,
            "label_key": metadata.get("label"),
            "parent": parent_id,
            "inputs": node.get("inputs", {}),
            "outputs": node.get("outputs", {}),
        }
        collected.append(node_summary)
        body = node.get("body")
        if isinstance(body, list):
            _gather_nodes(body, plugin_map, parent_id=node_id, collected=collected)
    return collected


def _build_edges(nodes: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    producers: Dict[str, str] = {}
    for node in nodes:
        outputs = node.get("outputs", {})
        for value in outputs.values():
            if isinstance(value, str):
                producers[value] = node["id"]
    edges: List[Dict[str, str]] = []
    for node in nodes:
        inputs = node.get("inputs", {})
        for port, value in inputs.items():
            if isinstance(value, str) and value.startswith("$"):
                variable = value[1:]
                source = producers.get(variable)
                if source:
                    edges.append({"from": source, "to": node["id"], "var": variable, "port": port})
    return edges


def build_workflow_graph() -> Dict[str, Any]:
    definition = _parse_workflow_definition()
    plugin_map = load_metadata().get("workflow_plugins", {})
    nodes = _gather_nodes(definition.get("nodes", []), plugin_map)
    edges = _build_edges(nodes)
    return {
        "nodes": nodes,
        "edges": edges,
        "count": {"nodes": len(nodes), "edges": len(edges)},
    }
