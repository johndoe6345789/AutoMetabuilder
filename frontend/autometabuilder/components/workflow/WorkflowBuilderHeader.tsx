import { Typography } from "@mui/material";

type WorkflowBuilderHeaderProps = {
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowBuilderHeader({ t }: WorkflowBuilderHeaderProps) {
  return (
    <>
      <Typography variant="h6" gutterBottom>
        {t("ui.workflow.canvas.title", "Visual Workflow Builder")}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 2 }}>
        {t("ui.workflow.canvas.subtitle", "Design workflows with an n8n-style visual canvas")}
      </Typography>
    </>
  );
}
