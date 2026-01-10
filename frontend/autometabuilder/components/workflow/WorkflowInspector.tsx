"use client";

import { Paper, Stack, Typography } from "@mui/material";

type WorkflowInspectorProps = {
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowInspector({ t }: WorkflowInspectorProps) {
  return (
    <Paper sx={{ p: 2, minHeight: 400, backgroundColor: "var(--color-panel-alt)" }}>
      <Typography variant="subtitle1" gutterBottom>
        {t("ui.workflow.inspector.title", "Inspector")}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {t(
          "ui.workflow.inspector.empty",
          "Select a node or edge to view and edit properties"
        )}
      </Typography>
      <Stack spacing={2} sx={{ mt: 2 }}>
        <Typography variant="caption" color="text.secondary">
          {t("ui.workflow.inspector.hint", "Node properties will appear here when selected")}
        </Typography>
      </Stack>
    </Paper>
  );
}
