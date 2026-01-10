"use client";

import { useEffect } from "react";
import { Alert, Snackbar } from "@mui/material";
import DashboardSection from "../components/sections/DashboardSection";
import PromptSection from "../components/sections/PromptSection";
import SettingsSection from "../components/sections/SettingsSection";
import TranslationsSection from "../components/sections/TranslationsSection";
import WorkflowSection from "../components/sections/WorkflowSection";
import PageLayout from "../components/layout/PageLayout";
import useDashboardContext from "../hooks/useDashboardContext";
import { emitWebhook, useWebhook } from "../hooks/useWebhook";
import { fetchWorkflowPackage, runBot, savePrompt, saveSettings, saveWorkflow } from "../lib/api";

export default function HomePage() {
  const {
    context,
    selectedSection,
    setSelectedSection,
    loading,
    error,
    snack,
    setSnack,
    snackOpen,
    setSnackOpen,
    ready,
    loadContext,
    t,
  } = useDashboardContext();

  useEffect(() => {
    void loadContext();
  }, [loadContext]);

  useWebhook(
    "botRunComplete",
    (detail) => {
      const mode = (detail as { mode?: string })?.mode ?? "once";
      setSnack(`Run finished: ${mode}`);
      setSnackOpen(true);
    },
    []
  );

  const handleRun = async (payload: Parameters<typeof runBot>[0]) => {
    await runBot(payload);
    emitWebhook("botRunComplete", payload);
    await loadContext();
  };

  if (isLoading) {
    return (
      <main className="app-loading">
        <p>Loading dashboard…</p>
      </main>
    );
  }

  if (error || !ready || !context) {
    return (
      <main className="app-loading">
        <p>{error || "Unable to load context."}</p>
        <button type="button" onClick={loadContext}>
          Retry
        </button>
      </main>
    );
  }

  return (
    <>
      <PageLayout navItems={context.navigation} section={selectedSection} onSectionChange={setSelectedSection} t={t}>
        {selectedSection === "dashboard" && (
          <DashboardSection logs={context.logs} status={context.status} onRun={handleRun} t={t} />
        )}
        {selectedSection === "workflow" && (
          <WorkflowSection
            content={context.workflow_content}
            packages={context.workflow_packages}
            onSave={async (content) => {
              await saveWorkflow(content);
              emitWebhook("workflow.save", { content });
              await loadContext();
            }}
            onTemplateSelect={async (id) => {
              const pkg = await fetchWorkflowPackage(id);
              if (pkg.workflow) {
                const workflowPayload = JSON.stringify(pkg.workflow ?? {}, null, 2);
                await saveWorkflow(workflowPayload);
                emitWebhook("workflow.template.selected", { id });
                await loadContext();
              }
            }}
            t={t}
          />
        )}
        {selectedSection === "prompt" && (
          <PromptSection
            content={context.prompt_content}
            onSave={async (content) => {
              await savePrompt(content);
              emitWebhook("prompt.save", { content });
              await loadContext();
            }}
            t={t}
          />
        )}
        {selectedSection === "settings" && (
          <SettingsSection
            envVars={context.env_vars}
            onSave={async (values) => {
              await saveSettings(values);
              emitWebhook("settings.save", { values });
              await loadContext();
            }}
            t={t}
          />
        )}
        {selectedSection === "translations" && <TranslationsSection languages={context.translations} onRefresh={loadContext} t={t} />}
      </PageLayout>
      <Snackbar open={snackOpen} autoHideDuration={4000} onClose={() => setSnackOpen(false)}>
        <Alert onClose={() => setSnackOpen(false)} severity="info" sx={{ width: "100%" }}>
          {snack}
        </Alert>
      </Snackbar>
    </>
  );
}
