import { Box, Chip, Stack, Typography } from "@mui/material";
import { WorkflowPluginDefinition, WorkflowPluginPort } from "../../lib/types";

type WorkflowPaletteCardProps = {
  id: string;
  plugin: WorkflowPluginDefinition;
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowPaletteCard({ id, plugin, t }: WorkflowPaletteCardProps) {
  const translateLabel = plugin.label ? t(plugin.label, id) : id;

  return (
    <Box sx={{ display: "flex", flexDirection: "column" }}>
      <Typography variant="subtitle2">{translateLabel}</Typography>
      <Typography variant="caption" color="text.secondary">
        {t("ui.workflow.node_id_label", "Node ID")}: {id}
      </Typography>
      <Stack direction="row" spacing={1} flexWrap="wrap" mt={1}>
        {renderPortChips(t, "in", plugin.inputs)}
        {renderPortChips(t, "out", plugin.outputs)}
      </Stack>
    </Box>
  );
}

function renderPortChips(
  t: (key: string, fallback?: string) => string,
  direction: "in" | "out",
  ports?: Record<string, WorkflowPluginPort>
) {
  if (!ports) {
    return null;
  }
  return Object.keys(ports).map((name) => {
    const port = ports[name];
    const portLabel = port?.label ? t(port.label, name) : name;
    return (
      <Chip
        key={`${direction}-${name}`}
        label={`${direction === "in" ? "⮂" : "⮀"} ${portLabel}`}
        size="small"
        sx={{ backgroundColor: "rgba(255,255,255,0.08)", color: "white" }}
      />
    );
  });
}
