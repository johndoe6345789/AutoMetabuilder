"use client";

import { Paper } from "@mui/material";
import { useWorkflowGraph } from "../../hooks/useWorkflowGraph";
import { useWorkflowPlugins } from "../../hooks/useWorkflowPlugins";
import { useTabNavigation } from "../../hooks/useTabNavigation";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";
import WorkflowBuilderHeader from "./WorkflowBuilderHeader";
import WorkflowBuilderTabs from "./WorkflowBuilderTabs";
import WorkflowBuilderContent from "./WorkflowBuilderContent";

type VisualWorkflowBuilderProps = {
  t: (key: string, fallback?: string) => string;
};

export default function VisualWorkflowBuilder({ t }: VisualWorkflowBuilderProps) {
  const { graph, loading: graphLoading, error: graphError } = useWorkflowGraph();
  const { plugins, loading: pluginsLoading, error: pluginsError } = useWorkflowPlugins();
  const { selectedTab, handleTabChange } = useTabNavigation(0);

  const error = graphError || pluginsError;
  const loading = graphLoading || pluginsLoading;

  if (error) {
    return <ErrorState message={error} />;
  }

  if (loading || !graph) {
    return <LoadingState message={t("ui.workflow.canvas.loading", "Loading workflow canvas...")} />;
  }

  return (
    <Paper sx={{ p: 3, backgroundColor: "var(--color-panel-bg)" }}>
      <WorkflowBuilderHeader t={t} />
      <WorkflowBuilderTabs value={selectedTab} onChange={handleTabChange} t={t} />
      <WorkflowBuilderContent selectedTab={selectedTab} graph={graph} plugins={plugins} t={t} />
    </Paper>
  );
}
