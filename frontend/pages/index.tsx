import { useEffect, useMemo, useState } from "react";
import DashboardSection from "../components/sections/DashboardSection";
import PromptSection from "../components/sections/PromptSection";
import SettingsSection from "../components/sections/SettingsSection";
import TranslationsSection from "../components/sections/TranslationsSection";
import WorkflowSection from "../components/sections/WorkflowSection";
import PageLayout from "../components/layout/PageLayout";
import {
  fetchContext,
  fetchWorkflowPackage,
  runBot,
  savePrompt,
  saveSettings,
  saveWorkflow,
} from "../lib/api";
import { UIContext } from "../lib/types";

export default function HomePage() {
  const [context, setContext] = useState<UIContext | null>(null);
  const [selectedSection, setSelectedSection] = useState("dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadContext = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchContext();
      setContext(data);
      setSelectedSection((prev) => prev ?? data.navigation[0]?.section ?? "dashboard");
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadContext();
  }, []);

  const t = useMemo(
    () => (key: string, fallback?: string) => context?.messages[key] ?? fallback ?? key,
    [context]
  );

  const handleRun = async (payload: Parameters<typeof runBot>[0]) => {
    await runBot(payload);
    await loadContext();
  };

  const handleWorkflowSave = async (content: string) => {
    await saveWorkflow(content);
    await loadContext();
  };

  const handleTemplateSelect = async (id: string) => {
    const pkg = await fetchWorkflowPackage(id);
    const workflowPayload = JSON.stringify(pkg.workflow ?? {}, null, 2);
    setContext((prev) => (prev ? { ...prev, workflow_content: workflowPayload } : prev));
  };

  const handlePromptSave = async (content: string) => {
    await savePrompt(content);
    await loadContext();
  };

  const handleSettingsSave = async (values: Record<string, string>) => {
    await saveSettings(values);
    await loadContext();
  };

  if (loading) {
    return (
      <main className="app-loading">
        <p>Loading dashboard…</p>
      </main>
    );
  }

  if (error || !context) {
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
    <PageLayout navItems={context.navigation} section={selectedSection} onSectionChange={setSelectedSection} t={t}>
      {selectedSection === "dashboard" && (
        <DashboardSection logs={context.logs} status={context.status} onRun={handleRun} t={t} />
      )}
      {selectedSection === "workflow" && (
        <WorkflowSection
          content={context.workflow_content}
          packages={context.workflow_packages}
          onSave={handleWorkflowSave}
          onTemplateSelect={handleTemplateSelect}
          t={t}
        />
      )}
      {selectedSection === "prompt" && <PromptSection content={context.prompt_content} onSave={handlePromptSave} t={t} />}
      {selectedSection === "settings" && (
        <SettingsSection envVars={context.env_vars} onSave={handleSettingsSave} t={t} />
      )}
      {selectedSection === "translations" && (
        <TranslationsSection languages={context.translations} onRefresh={loadContext} t={t} />
      )}
    </PageLayout>
  );
}
