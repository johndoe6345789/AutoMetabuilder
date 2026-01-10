"use client";

import ReactFlow, {
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  Panel,
  ReactFlowProvider,
} from "reactflow";
import "reactflow/dist/style.css";
import { Box } from "@mui/material";
import { WorkflowGraph, WorkflowPluginMap, Node, Edge } from "../../lib/types";
import WorkflowNode from "./WorkflowNode";
import CanvasInfoPanel from "./CanvasInfoPanel";
import CanvasHintPanel from "./CanvasHintPanel";
import { useWorkflowCanvas } from "../../hooks/useWorkflowCanvas";

const nodeTypes = {
  workflow: WorkflowNode,
};

type WorkflowCanvasProps = {
  graph: WorkflowGraph;
  plugins: WorkflowPluginMap;
  onNodesChange?: (nodes: Node[]) => void;
  onEdgesChange?: (edges: Edge[]) => void;
  t: (key: string, fallback?: string) => string;
};

function WorkflowCanvasInner(props: WorkflowCanvasProps) {
  const { graph, plugins, onNodesChange, onEdgesChange, t } = props;
  const {
    nodes,
    edges,
    onNodesChangeInternal,
    onEdgesChangeInternal,
    onConnect,
    onDragOver,
    onDrop,
    reactFlowWrapper,
  } = useWorkflowCanvas(graph, plugins, t, onNodesChange, onEdgesChange);

  return (
    <Box
      ref={reactFlowWrapper}
      sx={{ width: "100%", height: "600px", position: "relative" }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChangeInternal}
        onEdgesChange={onEdgesChangeInternal}
        onConnect={onConnect}
        onDragOver={onDragOver}
        onDrop={onDrop}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Background variant={BackgroundVariant.Dots} gap={16} size={1} />
        <Controls />
        <MiniMap
          nodeStrokeWidth={3}
          zoomable
          pannable
          style={{
            backgroundColor: "var(--color-panel-bg)",
            border: "1px solid var(--color-border-muted)",
          }}
        />
        <Panel position="top-left">
          <CanvasInfoPanel nodeCount={nodes.length} edgeCount={edges.length} t={t} />
        </Panel>
        <Panel position="top-right">
          <CanvasHintPanel t={t} />
        </Panel>
      </ReactFlow>
    </Box>
  );
}

export default function WorkflowCanvas(props: WorkflowCanvasProps) {
  return (
    <ReactFlowProvider>
      <WorkflowCanvasInner {...props} />
    </ReactFlowProvider>
  );
}

