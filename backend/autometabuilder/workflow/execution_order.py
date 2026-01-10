"""Build execution order for n8n workflows."""
from __future__ import annotations

from typing import Any, Dict, List, Set


def build_execution_order(
    nodes: List[Dict[str, Any]],
    connections: Dict[str, Any]
) -> List[str]:
    """Build topological execution order from connections."""
    node_names = {node["name"] for node in nodes}
    has_inputs = _find_nodes_with_inputs(connections)
    
    # Start with nodes that have no inputs
    order = [name for name in node_names if name not in has_inputs]
    
    # Add remaining nodes (simplified BFS)
    remaining = node_names - set(order)
    order.extend(_add_remaining_nodes(remaining))
    
    return order


def _find_nodes_with_inputs(connections: Dict[str, Any]) -> Set[str]:
    """Find all nodes that have incoming connections."""
    has_inputs = set()
    
    for source_name, outputs in connections.items():
        for output_type, indices in outputs.items():
            for targets in indices.values():
                for target in targets:
                    has_inputs.add(target["node"])
    
    return has_inputs


def _add_remaining_nodes(remaining: Set[str]) -> List[str]:
    """Add remaining nodes in order."""
    order = []
    while remaining:
        name = next(iter(remaining))
        order.append(name)
        remaining.remove(name)
    return order
