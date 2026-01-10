import DashboardSection from "./DashboardSection";
import PromptSection from "./PromptSection";
import SettingsSection from "./SettingsSection";
import TranslationsSection from "./TranslationsSection";
import WorkflowSection from "./WorkflowSection";
import { UIContext } from "../../lib/types";
import { DashboardRunPayload } from "../../hooks/useDashboardControls";

type DashboardSectionsProps = {
  section: string;
  context: UIContext;
  t: (key: string, fallback?: string) => string;
  onRun: (payload: DashboardRunPayload) => Promise<void>;
  onWorkflowSave: (content: string) => Promise<void>;
  onTemplateSelect: (id: string) => Promise<void>;
  onPromptSave: (content: string) => Promise<void>;
  onSettingsSave: (values: Record<string, string>) => Promise<void>;
  onTranslationsRefresh: () => void;
};

export default function DashboardSections({
  section,
  context,
  t,
  onRun,
  onWorkflowSave,
  onTemplateSelect,
  onPromptSave,
  onSettingsSave,
  onTranslationsRefresh,
}: DashboardSectionsProps) {
  return (
    <>
      {section === "dashboard" && <DashboardSection logs={context.logs} status={context.status} onRun={onRun} t={t} />}
      {section === "workflow" && (
        <WorkflowSection
          content={context.workflow_content}
          packages={context.workflow_packages}
          onSave={onWorkflowSave}
          onTemplateSelect={onTemplateSelect}
          t={t}
        />
      )}
      {section === "prompt" && <PromptSection content={context.prompt_content} onSave={onPromptSave} t={t} />}
      {section === "settings" && <SettingsSection envVars={context.env_vars} onSave={onSettingsSave} t={t} />}
      {section === "translations" && <TranslationsSection languages={context.translations} onRefresh={onTranslationsRefresh} t={t} />}
    </>
  );
}
