"""Build a node/edge view of the declarative workflow for visualization."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Iterable, List

from .data import get_workflow_content, load_metadata

logger = logging.getLogger(__name__)


def _parse_workflow_definition() -> Dict[str, Any]:
    payload = get_workflow_content()
    if not payload:
        return {"nodes": []}
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        logger.warning("Invalid workflow JSON: %s", exc)
        return {"nodes": []}
    return parsed if isinstance(parsed, dict) else {"nodes": []}


def _is_n8n_format(workflow: Dict[str, Any]) -> bool:
    """Check if workflow uses n8n schema."""
    if "connections" not in workflow:
        return False
    nodes = workflow.get("nodes", [])
    if nodes and isinstance(nodes, list):
        first_node = nodes[0]
        return "position" in first_node or "typeVersion" in first_node
    return True


def _gather_n8n_nodes(
    nodes: Iterable[Dict[str, Any]],
    plugin_map: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Extract nodes from n8n format."""
    collected = []
    for node in nodes:
        node_id = node.get("id", node.get("name", f"node-{len(collected)}"))
        node_type = node.get("type", "unknown")
        metadata = plugin_map.get(node_type, {})
        
        collected.append({
            "id": node_id,
            "name": node.get("name", node_id),
            "type": node_type,
            "label_key": metadata.get("label"),
            "parent": None,
            "position": node.get("position", [0, 0]),
        })
    return collected


def _build_n8n_edges(
    connections: Dict[str, Any],
    nodes: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """Build edges from n8n connections."""
    # Build name to ID mapping
    name_to_id = {node["name"]: node["id"] for node in nodes}
    
    edges = []
    for source_name, outputs in connections.items():
        source_id = name_to_id.get(source_name, source_name)
        
        for output_type, indices in outputs.items():
            for index, targets in indices.items():
                for target in targets:
                    target_name = target["node"]
                    target_id = name_to_id.get(target_name, target_name)
                    
                    edges.append({
                        "from": source_id,
                        "to": target_id,
                        "type": target.get("type", "main"),
                        "output_index": index,
                        "input_index": target.get("index", 0),
                    })
    return edges


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
                if value in producers:
                    logger.debug("Variable %s already produced by %s; overwriting with %s", value, producers[value], node["id"])
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
                else:
                    logger.debug("No producer found for %s referenced by %s.%s", variable, node["id"], port)
    return edges


def build_workflow_graph() -> Dict[str, Any]:
    definition = _parse_workflow_definition()
    plugin_map = load_metadata().get("workflow_plugins", {})
    
    # Detect format and build accordingly
    if _is_n8n_format(definition):
        nodes = _gather_n8n_nodes(definition.get("nodes", []), plugin_map)
        edges = _build_n8n_edges(definition.get("connections", {}), nodes)
    else:
        nodes = _gather_nodes(definition.get("nodes", []), plugin_map)
        edges = _build_edges(nodes)
    
    logger.debug("Built workflow graph with %d nodes and %d edges", len(nodes), len(edges))
    return {
        "nodes": nodes,
        "edges": edges,
        "count": {"nodes": len(nodes), "edges": len(edges)},
    }
