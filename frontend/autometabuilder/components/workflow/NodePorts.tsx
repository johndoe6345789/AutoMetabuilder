import { Handle, Position } from "reactflow";
import { WorkflowPluginPort } from "../../lib/types";

type NodePortsProps = {
  ports: WorkflowPluginPort[];
  type: "input" | "output";
};

export default function NodePorts({ ports, type }: NodePortsProps) {
  const isInput = type === "input";
  const position = isInput ? Position.Left : Position.Right;
  const handleType = isInput ? "target" : "source";

  return (
    <>
      {ports.map((port, index) => (
        <Handle
          key={`${type}-${port.key}`}
          type={handleType}
          position={position}
          id={port.key}
          style={{
            top: `${((index + 1) * 100) / (ports.length + 1)}%`,
            width: 10,
            height: 10,
            backgroundColor: port.required ? "#f44336" : isInput ? "#4caf50" : "#2196f3",
          }}
        />
      ))}
    </>
  );
}
