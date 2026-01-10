import { useEffect } from "react";
import { Node, useNodesState } from "reactflow";
import { WorkflowGraph, WorkflowPluginMap } from "../lib/types";

export function useCanvasNodes(
  graph: WorkflowGraph,
  plugins: WorkflowPluginMap,
  t: (key: string, fallback?: string) => string,
  onNodesChange?: (nodes: Node[]) => void
) {
  const [nodes, setNodes, onNodesChangeInternal] = useNodesState([]);

  useEffect(() => {
    const flowNodes: Node[] = graph.nodes.map((node, index) => {
      const plugin = plugins[node.type] || {};
      const x = (index % 5) * 250;
      const y = Math.floor(index / 5) * 150;

      return {
        id: node.id,
        type: "workflow",
        position: { x, y },
        data: {
          label: plugin.label ? t(plugin.label, node.type) : node.type,
          type: node.type,
          inputs: node.inputs || {},
          outputs: node.outputs || {},
          plugin,
          t,
        },
      };
    });

    setNodes(flowNodes);
  }, [graph, plugins, t, setNodes]);

  useEffect(() => {
    if (onNodesChange) onNodesChange(nodes);
  }, [nodes, onNodesChange]);

  return { nodes, setNodes, onNodesChangeInternal };
}
