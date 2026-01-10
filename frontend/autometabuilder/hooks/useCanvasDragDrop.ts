import { useCallback, DragEvent, useRef } from "react";
import { Node, useReactFlow } from "reactflow";
import { WorkflowPluginMap } from "../lib/types";

export function useCanvasDragDrop(
  plugins: WorkflowPluginMap,
  t: (key: string, fallback?: string) => string,
  onNodeAdd: (node: Node) => void
) {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { project } = useReactFlow();

  const onDragOver = useCallback((event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback(
    (event: DragEvent<HTMLDivElement>) => {
      event.preventDefault();

      const type = event.dataTransfer.getData("application/reactflow");
      if (!type || !reactFlowWrapper.current) {
        return;
      }

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const position = project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const plugin = plugins[type] || {};
      const newNode: Node = {
        id: `node-${Date.now()}`,
        type: "workflow",
        position,
        data: {
          label: plugin.label ? t(plugin.label, type) : type,
          type,
          inputs: {},
          outputs: {},
          plugin,
          t,
        },
      };

      onNodeAdd(newNode);
    },
    [plugins, project, t, onNodeAdd]
  );

  return { onDragOver, onDrop, reactFlowWrapper };
}
