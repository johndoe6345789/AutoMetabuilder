import { useCallback } from "react";
import { emitWebhook } from "./useWebhook";
import { fetchWorkflowPackage, runBot, savePrompt, saveSettings, saveWorkflow } from "../lib/api";
import { DashboardRunPayload } from "./useDashboardControls";

type UseDashboardActionsArgs = {
  loadContext: () => Promise<void>;
};

type UseDashboardActionsResult = {
  handleRun: (payload: DashboardRunPayload) => Promise<void>;
  handleWorkflowSave: (content: string) => Promise<void>;
  handleTemplateSelect: (id: string) => Promise<void>;
  handlePromptSave: (content: string) => Promise<void>;
  handleSettingsSave: (values: Record<string, string>) => Promise<void>;
};

export default function useDashboardActions({ loadContext }: UseDashboardActionsArgs): UseDashboardActionsResult {
  const handleRun = useCallback(
    async (payload: DashboardRunPayload) => {
      await runBot(payload);
      emitWebhook("botRunComplete", payload);
      await loadContext();
    },
    [loadContext]
  );

  const handleWorkflowSave = useCallback(
    async (content: string) => {
      await saveWorkflow(content);
      emitWebhook("workflow.save", { content });
      await loadContext();
    },
    [loadContext]
  );

  const handleTemplateSelect = useCallback(
    async (id: string) => {
      const pkg = await fetchWorkflowPackage(id);
      if (pkg.workflow) {
        const workflowPayload = JSON.stringify(pkg.workflow ?? {}, null, 2);
        await saveWorkflow(workflowPayload);
        emitWebhook("workflow.template.selected", { id });
        await loadContext();
      }
    },
    [loadContext]
  );

  const handlePromptSave = useCallback(
    async (content: string) => {
      await savePrompt(content);
      emitWebhook("prompt.save", { content });
      await loadContext();
    },
    [loadContext]
  );

  const handleSettingsSave = useCallback(
    async (values: Record<string, string>) => {
      await saveSettings(values);
      emitWebhook("settings.save", { values });
      await loadContext();
    },
    [loadContext]
  );

  return {
    handleRun,
    handleWorkflowSave,
    handleTemplateSelect,
    handlePromptSave,
    handleSettingsSave,
  };
}
