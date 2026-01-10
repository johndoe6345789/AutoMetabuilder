import { useEffect, useState } from "react";

type SettingsSectionProps = {
  envVars: Record<string, string>;
  onSave: (values: Record<string, string>) => Promise<void>;
  t: (key: string, fallback?: string) => string;
};

export default function SettingsSection({ envVars, onSave, t }: SettingsSectionProps) {
  const [values, setValues] = useState<Record<string, string>>(envVars);
  const [newKey, setNewKey] = useState("");
  const [newValue, setNewValue] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    setValues(envVars);
  }, [envVars]);

  const updateField = (key: string, next: string) => {
    setValues((prev) => ({ ...prev, [key]: next }));
  };

  const handleSave = async () => {
    await onSave(values);
    setMessage(t("ui.settings.save_all", "Save All Settings"));
    setTimeout(() => setMessage(""), 2000);
  };

  const handleAdd = () => {
    if (!newKey.trim()) return;
    updateField(newKey.trim(), newValue);
    setNewKey("");
    setNewValue("");
  };

  return (
    <section className="section-card" id="settings">
      <div className="section-card__header">
        <h2>{t("ui.settings.title", "Settings")}</h2>
        <p>{t("ui.settings.subtitle", "Configure services, security, and environment preferences")}</p>
      </div>
      <div className="settings-grid">
        {Object.entries(values).map(([key, value]) => (
          <label key={key} className="field-group">
            <span>{key}</span>
            <input value={value} onChange={(event) => updateField(key, event.target.value)} />
          </label>
        ))}
      </div>
      <div className="settings-grid settings-grid--new">
        <input placeholder={t("ui.settings.add.placeholder_key", "KEY")} value={newKey} onChange={(event) => setNewKey(event.target.value)} />
        <input placeholder={t("ui.settings.add.placeholder_value", "Value")} value={newValue} onChange={(event) => setNewValue(event.target.value)} />
        <button type="button" onClick={handleAdd}>
          {t("ui.actions.add", "Add")}
        </button>
      </div>
      <div className="workflow-actions">
        <button className="primary" type="button" onClick={handleSave}>
          {t("ui.settings.save_all", "Save All Settings")}
        </button>
        <span className="workflow-message">{message}</span>
      </div>
    </section>
  );
}
