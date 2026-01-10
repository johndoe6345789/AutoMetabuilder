import { useCallback } from "react";
import { Node, Edge } from "reactflow";
import { WorkflowGraph, WorkflowPluginMap } from "../../lib/types";
import { useCanvasNodes } from "./useCanvasNodes";
import { useCanvasEdges } from "./useCanvasEdges";
import { useCanvasDragDrop } from "./useCanvasDragDrop";

export function useWorkflowCanvas(
  graph: WorkflowGraph,
  plugins: WorkflowPluginMap,
  t: (key: string, fallback?: string) => string,
  onNodesChange?: (nodes: Node[]) => void,
  onEdgesChange?: (edges: Edge[]) => void
) {
  const { nodes, setNodes, onNodesChangeInternal } = useCanvasNodes(
    graph,
    plugins,
    t,
    onNodesChange
  );

  const { edges, onConnect, onEdgesChangeInternal } = useCanvasEdges(graph, onEdgesChange);

  const handleNodeAdd = useCallback(
    (node: Node) => {
      setNodes((nds) => nds.concat(node));
    },
    [setNodes]
  );

  const { onDragOver, onDrop, reactFlowWrapper } = useCanvasDragDrop(plugins, t, handleNodeAdd);

  return {
    nodes,
    edges,
    onNodesChangeInternal,
    onEdgesChangeInternal,
    onConnect,
    onDragOver,
    onDrop,
    reactFlowWrapper,
  };
}
