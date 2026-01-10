import { Divider, Paper, Stack, TextField, Typography } from "@mui/material";
import { useWorkflowPlugins } from "../../hooks/useWorkflowPlugins";
import { usePluginSearch } from "../../hooks/usePluginSearch";
import DraggablePaletteCard from "./DraggablePaletteCard";

type WorkflowPaletteProps = {
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowPalette({ t }: WorkflowPaletteProps) {
  const { plugins, loading, error } = useWorkflowPlugins();
  const { search, setSearch, filteredPlugins } = usePluginSearch(plugins, t);

  const hasQuery = search.trim().length > 0;

  if (error) {
    return (
      <Paper sx={{ p: 2, backgroundColor: "var(--color-panel-alt)" }}>
        <Typography color="error">{error}</Typography>
      </Paper>
    );
  }

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
      {loading ? (
        <Typography variant="caption" color="text.secondary">
          {t("ui.workflow.palette.loading", "Loading node library…")}
        </Typography>
      ) : filteredPlugins.length === 0 && hasQuery ? (
        <Typography variant="caption" color="text.secondary">
          {`${t("ui.workflow.palette.empty", "No matching nodes.")} "${search.trim()}"`}
        </Typography>
      ) : (
        <Stack spacing={1} divider={<Divider sx={{ borderColor: "var(--color-divider)" }} />}>
          {filteredPlugins.map(([id, plugin]) => (
            <DraggablePaletteCard key={id} id={id} plugin={plugin} t={t} />
          ))}
        </Stack>
      )}
    </Paper>
  );
}
