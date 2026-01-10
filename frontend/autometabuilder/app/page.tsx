"use client";

import { useEffect } from "react";
import { Alert, Snackbar } from "@mui/material";
import PageLayout from "../components/layout/PageLayout";
import DashboardSections from "../components/sections/DashboardSections";
import useDashboardContext from "../hooks/useDashboardContext";
import useDashboardActions from "../hooks/useDashboardActions";
import { useWebhook } from "../hooks/useWebhook";

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

  const { handleRun, handleWorkflowSave, handleTemplateSelect, handlePromptSave, handleSettingsSave } = useDashboardActions({
    loadContext,
  });

  if (loading) {
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
        <DashboardSections
          section={selectedSection}
          context={context}
          onRun={handleRun}
          onWorkflowSave={handleWorkflowSave}
          onTemplateSelect={handleTemplateSelect}
          onPromptSave={handlePromptSave}
          onSettingsSave={handleSettingsSave}
          onTranslationsRefresh={loadContext}
          t={t}
        />
      </PageLayout>
      <Snackbar open={snackOpen} autoHideDuration={4000} onClose={() => setSnackOpen(false)}>
        <Alert onClose={() => setSnackOpen(false)} severity="info" sx={{ width: "100%" }}>
          {snack}
        </Alert>
      </Snackbar>
    </>
  );
}
