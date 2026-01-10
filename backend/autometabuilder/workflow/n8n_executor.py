"""Execute n8n-style workflows with explicit connections."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class N8NExecutor:
    """Execute n8n-style workflows."""
    
    def __init__(self, runtime, plugin_registry):
        self.runtime = runtime
        self.plugin_registry = plugin_registry
    
    def execute(self, workflow: Dict[str, Any]) -> None:
        """Execute n8n workflow."""
        nodes = workflow.get("nodes", [])
        connections = workflow.get("connections", {})
        
        if not nodes:
            logger.warning("No nodes in workflow")
            return
        
        # Build execution order from connections
        execution_order = self._build_execution_order(nodes, connections)
        
        # Execute nodes in order
        for node_name in execution_order:
            node = self._find_node_by_name(nodes, node_name)
            if node:
                self._execute_node(node)
    
    def _find_node_by_name(self, nodes: List[Dict], name: str) -> Dict | None:
        """Find node by name."""
        for node in nodes:
            if node.get("name") == name:
                return node
        return None
    
    def _build_execution_order(
        self, 
        nodes: List[Dict],
        connections: Dict[str, Any]
    ) -> List[str]:
        """Build topological execution order."""
        # Simple approach: find nodes with no inputs, then process
        node_names = {node["name"] for node in nodes}
        has_inputs = set()
        
        for source_name, outputs in connections.items():
            for output_type, indices in outputs.items():
                for targets in indices.values():
                    for target in targets:
                        has_inputs.add(target["node"])
        
        # Start with nodes that have no inputs
        order = [name for name in node_names if name not in has_inputs]
        
        # Add remaining nodes (simplified BFS)
        remaining = node_names - set(order)
        while remaining:
            added = False
            for name in list(remaining):
                order.append(name)
                remaining.remove(name)
                added = True
                break
            if not added:
                break
        
        return order
    
    def _execute_node(self, node: Dict[str, Any]) -> Any:
        """Execute single node."""
        node_type = node.get("type")
        node_name = node.get("name", node.get("id"))
        
        if node.get("disabled"):
            logger.debug("Node %s is disabled, skipping", node_name)
            return None
        
        if node_type == "control.loop":
            return self._execute_loop(node)
        
        plugin = self.plugin_registry.get(node_type)
        if not plugin:
            logger.error("Unknown node type: %s", node_type)
            return None
        
        inputs = node.get("parameters", {})
        logger.debug("Executing node %s (%s)", node_name, node_type)
        
        result = plugin(self.runtime, inputs)
        return result
    
    def _execute_loop(self, node: Dict[str, Any]) -> Any:
        """Execute loop node (placeholder)."""
        logger.debug("Loop execution not yet implemented in n8n executor")
        return None
