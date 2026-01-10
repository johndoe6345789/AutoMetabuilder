import { FormEvent, useEffect, useState } from "react";
import {
  createTranslation,
  deleteTranslation,
  fetchTranslation,
  updateTranslation,
} from "../../lib/api";

type TranslationsSectionProps = {
  languages: Record<string, string>;
  onRefresh: () => void;
  t: (key: string, fallback?: string) => string;
};

export default function TranslationsSection({ languages, onRefresh, t }: TranslationsSectionProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const [editorValue, setEditorValue] = useState("{}");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [newLang, setNewLang] = useState("");

  const loadContent = async (lang: string) => {
    setError("");
    const data = await fetchTranslation(lang);
    setEditorValue(JSON.stringify(data.content, null, 2));
  };

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!selected && Object.keys(languages).length) {
      setSelected(Object.keys(languages)[0]);
    }
  }, [languages, selected]);

  useEffect(() => {
    if (selected) {
      loadContent(selected);
    }
  }, [selected]);
  /* eslint-enable react-hooks/set-state-in-effect */

  const handleSave = async () => {
    if (!selected) return;
    try {
      const payload = JSON.parse(editorValue);
      await updateTranslation(selected, payload);
      setMessage(t("ui.translations.notice.saved", "Translation saved!"));
      onRefresh();
    } catch (err) {
      setError(String(err));
    }
  };

  const handleCreate = async (event: FormEvent) => {
    event.preventDefault();
    if (!newLang.trim()) return;
    await createTranslation(newLang.trim());
    setNewLang("");
    onRefresh();
  };

  const handleDelete = async () => {
    if (!selected) return;
    await deleteTranslation(selected);
    setSelected(null);
    onRefresh();
  };

  return (
    <section className="section-card" id="translations">
      <div className="section-card__header">
        <h2>{t("ui.translations.title", "Translations")}</h2>
        <p>{t("ui.translations.subtitle", "Create, edit, and maintain language files for bot messages")}</p>
      </div>
      <div className="translations-layout">
        <div className="language-list">
          {Object.entries(languages).map(([lang, label]) => (
            <button
              key={lang}
              type="button"
              className={`language-chip ${selected === lang ? "active" : ""}`}
              onClick={() => setSelected(lang)}
            >
              {lang}
              <span>{`(${label})`}</span>
            </button>
          ))}
        </div>
        <textarea value={editorValue} onChange={(event) => setEditorValue(event.target.value)} rows={12} />
      </div>
      <div className="translations-actions">
        <button className="primary" type="button" onClick={handleSave} disabled={!selected}>
          {t("ui.actions.save", "Save")}
        </button>
        <button type="button" onClick={handleDelete} disabled={!selected}>
          {t("ui.actions.delete", "Delete")}
        </button>
        <form onSubmit={handleCreate} className="language-form">
          <input placeholder={t("ui.translations.add_language_placeholder", "Add language...")} value={newLang} onChange={(event) => setNewLang(event.target.value)} />
          <button type="submit">{t("ui.actions.add", "Add")}</button>
        </form>
      </div>
      {message && <p className="workflow-message">{message}</p>}
      {error && <p className="workflow-error">{error}</p>}
    </section>
  );
}
