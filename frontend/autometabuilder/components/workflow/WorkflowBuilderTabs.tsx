import { Tab, Tabs } from "@mui/material";

type WorkflowBuilderTabsProps = {
  value: number;
  onChange: (event: unknown, value: number) => void;
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowBuilderTabs({ value, onChange, t }: WorkflowBuilderTabsProps) {
  return (
    <Tabs value={value} onChange={onChange} sx={{ mb: 2 }}>
      <Tab label={t("ui.workflow.canvas.tab.canvas", "Canvas")} />
      <Tab label={t("ui.workflow.canvas.tab.inspector", "Inspector")} />
    </Tabs>
  );
}
