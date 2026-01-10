import { useEffect, useState } from "react";
import { Box, Button, Paper, Stack, Typography } from "@mui/material";
import { WorkflowPackageSummary } from "../../lib/types";
import WorkflowGraphPanel from "../workflow/WorkflowGraphPanel";
import WorkflowPalette from "../workflow/WorkflowPalette";

type WorkflowSectionProps = {
  content: string;
  packages: WorkflowPackageSummary[];
  onSave: (content: string) => Promise<void>;
  onTemplateSelect: (id: string) => void;
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowSection({ content, packages, onSave, onTemplateSelect, t }: WorkflowSectionProps) {
  const [draft, setDraft] = useState(content);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setDraft(content);
  }, [content]);

  const handleSave = async () => {
    await onSave(draft);
    setMessage(t("ui.workflow.save", "Save Workflow") + " " + t("ui.actions.save", "Save"));
    setTimeout(() => setMessage(""), 2000);
  };

  return (
    <Paper id="workflow" sx={{ p: 3, mb: 3, backgroundColor: "var(--color-panel-bg)" }}>
      <Typography variant="h5" gutterBottom>
        {t("ui.workflow.title", "Workflow Builder")}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {t("ui.workflow.subtitle", "Design the bot's task execution pipeline")}
      </Typography>
      <Stack direction={{ xs: "column", md: "row" }} spacing={3}>
        <Box sx={{ flex: 1 }}>
          <Box
            component="textarea"
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            rows={18}
            sx={{
              width: "100%",
              fontFamily: "JetBrains Mono, monospace",
              backgroundColor: "var(--color-input-bg)",
              border: "1px solid var(--color-border-muted)",
              borderRadius: 2,
              color: "var(--color-text-strong)",
              p: 2,
            }}
          />
          <Stack direction="row" spacing={1} alignItems="center" mt={2}>
            <Button variant="contained" onClick={handleSave}>
              {t("ui.workflow.save", "Save Workflow")}
            </Button>
            <Typography variant="body2" color="success.main">
              {message}
            </Typography>
          </Stack>
        </Box>
        <Paper sx={{ flex: 1, p: 2, backgroundColor: "var(--color-panel-alt)" }}>
          <Stack spacing={2}>
            <Box>
              <Typography variant="subtitle1" gutterBottom>
                {t("ui.workflow.templates.title", "Workflow Templates")}
              </Typography>
              <Stack spacing={1}>
                {packages.map((pkg) => (
                  <Paper key={pkg.id} variant="outlined" sx={{ p: 1 }}>
                    <Stack spacing={1}>
                      <Typography variant="subtitle2">{pkg.label}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {pkg.description}
                      </Typography>
                      <Button size="small" variant="text" onClick={() => onTemplateSelect(pkg.id)}>
                        {t("ui.workflow.templates.apply", "Apply Template")}
                      </Button>
                    </Stack>
                  </Paper>
                ))}
              </Stack>
            </Box>
            <WorkflowGraphPanel t={t} />
            <WorkflowPalette t={t} />
          </Stack>
        </Paper>
      </Stack>
    </Paper>
  );
}
