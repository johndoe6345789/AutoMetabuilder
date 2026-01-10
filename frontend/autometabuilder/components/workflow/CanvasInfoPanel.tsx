import { Paper, Typography } from "@mui/material";

type CanvasInfoPanelProps = {
  nodeCount: number;
  edgeCount: number;
  t: (key: string, fallback?: string) => string;
};

export default function CanvasInfoPanel({ nodeCount, edgeCount, t }: CanvasInfoPanelProps) {
  return (
    <Paper sx={{ p: 1, backgroundColor: "var(--color-panel-bg)" }}>
      <Typography variant="caption" color="text.secondary">
        {t("ui.workflow.canvas.info", "Nodes: {nodes}, Edges: {edges}")
          .replace("{nodes}", String(nodeCount))
          .replace("{edges}", String(edgeCount))}
      </Typography>
    </Paper>
  );
}
