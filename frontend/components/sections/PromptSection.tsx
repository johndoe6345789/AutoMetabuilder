import { useEffect, useState } from "react";

type PromptSectionProps = {
  content: string;
  onSave: (content: string) => Promise<void>;
  t: (key: string, fallback?: string) => string;
};

export default function PromptSection({ content, onSave, t }: PromptSectionProps) {
  const [draft, setDraft] = useState(content);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setDraft(content);
  }, [content]);

  const handleSave = async () => {
    await onSave(draft);
    setMessage(t("ui.prompt.save", "Save Prompt"));
    setTimeout(() => setMessage(""), 2000);
  };

  return (
    <section className="section-card" id="prompt">
      <div className="section-card__header">
        <h2>{t("ui.prompt.title", "Prompt Builder")}</h2>
        <p>{t("ui.prompt.subtitle", "Shape how the assistant thinks, speaks, and decides")}</p>
      </div>
      <textarea className="prompt-editor" value={draft} onChange={(event) => setDraft(event.target.value)} rows={12} />
      <div className="workflow-actions">
        <button className="primary" type="button" onClick={handleSave}>
          {t("ui.prompt.save", "Save Prompt")}
        </button>
        <span className="workflow-message">{message}</span>
      </div>
    </section>
  );
}
