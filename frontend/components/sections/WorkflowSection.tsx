import { useEffect, useState } from "react";
import { WorkflowPackageSummary } from "../../lib/types";

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
    <section className="section-card" id="workflow">
      <div className="section-card__header">
        <h2>{t("ui.workflow.title", "Workflow Builder")}</h2>
        <p>{t("ui.workflow.subtitle", "Design the bot's task execution pipeline")}</p>
      </div>
      <div className="workflow-grid">
        <div className="workflow-editor">
          <textarea value={draft} onChange={(event) => setDraft(event.target.value)} />
          <div className="workflow-actions">
            <button type="button" className="primary" onClick={handleSave}>
              {t("ui.workflow.save", "Save Workflow")}
            </button>
            <span className="workflow-message">{message}</span>
          </div>
        </div>
        <div className="workflow-templates">
          <h3>{t("ui.workflow.templates.title", "Workflow Templates")}</h3>
          <div className="template-palette">
            {packages.map((pkg) => (
              <article key={pkg.id} className="template-card">
                <div>
                  <strong>{pkg.label}</strong>
                  <p>{pkg.description}</p>
                </div>
                <button type="button" onClick={() => onTemplateSelect(pkg.id)}>
                  {t("ui.workflow.templates.apply", "Apply Template")}
                </button>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
