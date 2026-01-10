import { useCallback, useEffect } from "react";
import { Edge, Connection, addEdge, useEdgesState } from "reactflow";
import { WorkflowGraph } from "../lib/types";

export function useCanvasEdges(
  graph: WorkflowGraph,
  onEdgesChange?: (edges: Edge[]) => void
) {
  const [edges, setEdges, onEdgesChangeInternal] = useEdgesState([]);

  useEffect(() => {
    const flowEdges: Edge[] = graph.edges.map((edge, index) => ({
      id: `e-${edge.from}-${edge.to}-${edge.var}-${index}`,
      source: edge.from,
      target: edge.to,
      label: edge.var,
      type: "smoothstep",
      animated: false,
    }));

    setEdges(flowEdges);
  }, [graph, setEdges]);

  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((eds) => addEdge({ ...connection, type: "smoothstep" }, eds));
    },
    [setEdges]
  );

  useEffect(() => {
    if (onEdgesChange) onEdgesChange(edges);
  }, [edges, onEdgesChange]);

  return { edges, onConnect, onEdgesChangeInternal };
}
