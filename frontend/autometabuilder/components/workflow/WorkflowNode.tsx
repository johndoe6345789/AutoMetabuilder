"use client";

import { memo } from "react";
import { NodeProps } from "reactflow";
import { Paper, Stack } from "@mui/material";
import { WorkflowPluginDefinition } from "../../lib/types";
import NodeHeader from "./NodeHeader";
import NodeBody from "./NodeBody";
import NodePorts from "./NodePorts";

export type WorkflowNodeData = {
  label: string;
  type: string;
  inputs: Record<string, unknown>;
  outputs: Record<string, unknown>;
  plugin: WorkflowPluginDefinition;
  t: (key: string, fallback?: string) => string;
};

function WorkflowNode({ data, selected }: NodeProps<WorkflowNodeData>) {
  const { label, type, plugin, t } = data;
  const inputPorts = plugin.inputs || [];
  const outputPorts = plugin.outputs || [];

  return (
    <Paper
      elevation={selected ? 8 : 2}
      sx={{
        minWidth: 200,
        minHeight: 80,
        border: selected ? "2px solid #1976d2" : "1px solid var(--color-border-muted)",
        backgroundColor: "var(--color-panel-bg)",
        transition: "all 0.2s",
        "&:hover": {
          boxShadow: 4,
        },
      }}
    >
      <NodePorts ports={inputPorts} type="input" />

      <Stack spacing={1} sx={{ p: 1.5 }}>
        <NodeHeader type={type} />
        <NodeBody
          label={label}
          category={plugin.category}
          inputCount={inputPorts.length}
          outputCount={outputPorts.length}
          t={t}
        />
      </Stack>

      <NodePorts ports={outputPorts} type="output" />
    </Paper>
  );
}

export default memo(WorkflowNode);
