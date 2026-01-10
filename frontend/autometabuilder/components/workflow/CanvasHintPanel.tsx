import { Paper, Typography } from "@mui/material";

type CanvasHintPanelProps = {
  t: (key: string, fallback?: string) => string;
};

export default function CanvasHintPanel({ t }: CanvasHintPanelProps) {
  return (
    <Paper sx={{ p: 1, backgroundColor: "var(--color-panel-bg)" }}>
      <Typography variant="caption" color="text.secondary">
        {t("ui.workflow.canvas.hint", "Drag nodes from palette to add")}
      </Typography>
    </Paper>
  );
}
