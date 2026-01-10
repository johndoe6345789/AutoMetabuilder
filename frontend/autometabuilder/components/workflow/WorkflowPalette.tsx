import { useEffect, useMemo, useState } from "react";
import { Box, Chip, Divider, Paper, Stack, TextField, Typography } from "@mui/material";
import { fetchWorkflowPlugins } from "../../lib/api";
import { WorkflowPluginDefinition, WorkflowPluginMap, WorkflowPluginPort } from "../../lib/types";

type WorkflowPaletteProps = {
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowPalette({ t }: WorkflowPaletteProps) {
  const [plugins, setPlugins] = useState<WorkflowPluginMap>({});
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let alive = true;
    void fetchWorkflowPlugins()
      .then((data) => {
        if (alive) {
          setPlugins(data);
        }
      })
      .catch((err) => {
        if (alive) {
          setError(String(err));
        }
      });
    return () => {
      alive = false;
    };
  }, []);

  const entries = useMemo(() => {
    const query = search.trim().toLowerCase();
    return Object.entries(plugins).filter(([id, plugin]) => {
      const label = plugin.label ? t(plugin.label, id) : id;
      return !query || `${id} ${label}`.toLowerCase().includes(query);
    });
  }, [plugins, search, t]);

  const isLoading = entries.length === 0 && !search && !error;
  const hasQuery = search.trim().length > 0;

  return (
    <Paper sx={{ p: 2, backgroundColor: "#0b1221" }}>
      <Typography variant="subtitle1" gutterBottom>
        {t("ui.workflow.palette.title", "Workflow Palette")}
      </Typography>
      <TextField
        size="small"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder={t("ui.workflow.palette.search_placeholder", "Search nodes or keywords...")}
        fullWidth
        sx={{ mb: 2 }}
      />
      {error ? (
        <Typography color="error">{error}</Typography>
      ) : isLoading ? (
        <Typography variant="caption" color="text.secondary">
          {t("ui.workflow.palette.loading", "Loading node library…")}
        </Typography>
      ) : entries.length === 0 && hasQuery ? (
        <Typography variant="caption" color="text.secondary">
          {t("ui.workflow.palette.missing", "No nodes match \"{query}\"").replace("{query}", search.trim())}
        </Typography>
      ) : (
        <Stack spacing={1} divider={<Divider sx={{ borderColor: "rgba(255,255,255,0.08)" }} />}>
          {entries.map(([id, plugin]) => (
            <Box key={id} sx={{ display: "flex", flexDirection: "column" }}>
              <Typography variant="subtitle2">
                {plugin.label ? t(plugin.label, id) : id}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {t("ui.workflow.palette.node_id", "Node ID")}: {id}
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" mt={1}>
                {renderPortTags(t, "in", plugin.inputs)}
                {renderPortTags(t, "out", plugin.outputs)}
              </Stack>
            </Box>
          ))}
        </Stack>
      )}
    </Paper>
  );
}

function renderPortTags(
  t: (key: string, fallback?: string) => string,
  direction: "in" | "out",
  ports?: Record<string, WorkflowPluginPort>
) {
  if (!ports) {
    return null;
  }
  return Object.keys(ports).map((name) => {
    const port = ports[name];
    const label = port?.label ? t(port.label, name) : name;
    return (
      <Chip
        key={`${direction}-${name}`}
        label={`${direction === "in" ? "⮂" : "⮀"} ${label}`}
        size="small"
        sx={{ backgroundColor: "rgba(255,255,255,0.08)", color: "white" }}
      />
    );
  });
}
