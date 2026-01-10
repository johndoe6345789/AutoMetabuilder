import { useEffect, useMemo, useState } from "react";
import { Divider, Paper, Stack, TextField, Typography } from "@mui/material";
import { fetchWorkflowPlugins } from "../../lib/api";
import { WorkflowPluginMap } from "../../lib/types";
import WorkflowPaletteCard from "./WorkflowPaletteCard";

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
    <Paper sx={{ p: 2, backgroundColor: "var(--color-panel-alt)" }}>
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
          {`${t("ui.workflow.palette.empty", "No matching nodes.")} "${search.trim()}"`}
        </Typography>
      ) : (
        <Stack spacing={1} divider={<Divider sx={{ borderColor: "var(--color-divider)" }} />}>
          {entries.map(([id, plugin]) => (
            <WorkflowPaletteCard key={id} id={id} plugin={plugin} t={t} />
          ))}
        </Stack>
      )}
    </Paper>
  );
}
