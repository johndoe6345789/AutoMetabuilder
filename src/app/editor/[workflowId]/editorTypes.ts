/**
 * editorTypes - Shared type definitions for the workflow editor
 */

import type {
  RefObject,
  DragEvent,
  Dispatch,
  SetStateAction,
} from 'react';
import type { NodeType } from '@metabuilder/components/workflow-editor';
// Owned by the hook that produces it. This module previously redeclared it with
// startNodeId/startPort, names nothing at runtime ever set - useNodeConnections
// reads sourceNodeId/sourceOutput - so the duplicate was silently wrong.
import type { DrawingConnection } from './hooks/useDrawingConnection';
import type {
  WorkflowNode,
  Connection as WorkflowConnection,
} from '@metabuilder/hooks/workflow-editor';

export interface UseCanvasPanInput {
  canvasOffset: { x: number; y: number };
  setCanvasOffset: (v: { x: number; y: number }) => void;
  zoom: number;
  drawingConnection: DrawingConnection | null;
  setDrawingConnection: Dispatch<
    SetStateAction<DrawingConnection | null>
  >;
  canvasRef: RefObject<HTMLDivElement>;
}

export type { DrawingConnection };

export interface EditorCanvasAreaProps {
  canvasRef: RefObject<HTMLDivElement>;
  canvasOffset: { x: number; y: number };
  zoom: number;
  isPanning: boolean;
  nodes: WorkflowNode[];
  connections: WorkflowConnection[];
  drawingConnection: DrawingConnection | null;
  selectedNodeId: string | null;
  onCanvasDrop: (e: DragEvent<HTMLDivElement>) => void;
  onCanvasDragOver: (e: DragEvent<HTMLDivElement>) => void;
  onCanvasMouseDown: (
    e: React.MouseEvent<HTMLDivElement>
  ) => void;
  onWheel: (e: React.WheelEvent<HTMLDivElement>) => void;
  onNodeSelect: (id: string) => void;
  onNodeDoubleClick: (id: string) => void;
  // useNodeDrag derives the offset from the event itself, and the library's
  // CanvasNode calls this with two arguments; the offsets were never passed.
  onNodeDragStart: (e: React.MouseEvent, id: string) => void;
  onConnectionStart: (
    nodeId: string,
    port: string,
    position: { x: number; y: number }
  ) => void;
  onConnectionEnd: (nodeId: string, port: string) => void;
  getNodeType: (type: string) => NodeType | undefined;
}
