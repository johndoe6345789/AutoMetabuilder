import { useEffect, useState } from "react";
import { Button, Paper, Stack, TextField, Typography } from "@mui/material";

type SettingsSectionProps = {
  envVars: Record<string, string>;
  onSave: (values: Record<string, string>) => Promise<void>;
  t: (key: string, fallback?: string) => string;
  active: boolean;
};

export default function SettingsSection({ envVars, onSave, t, active }: SettingsSectionProps) {
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
    <Paper
      id="settings"
      className={active ? "active" : ""}
      sx={{ p: 3, mb: 3, backgroundColor: "var(--color-panel-bg)", display: active ? "block" : "none" }}
    >
      <Typography variant="h5" gutterBottom>
        {t("ui.settings.title", "Settings")}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {t("ui.settings.subtitle", "Configure services, security, and environment preferences")}
      </Typography>
      <Stack spacing={2} mt={2}>
        {Object.entries(values).map(([key, value]) => (
          <TextField
            key={key}
            label={key}
            value={value}
            onChange={(event) => updateField(key, event.target.value)}
            InputProps={{
              sx: {
                backgroundColor: "var(--color-input-bg)",
                borderRadius: 1,
                color: "var(--color-text-strong)",
              },
            }}
          />
        ))}
      </Stack>
      <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mt: 2 }}>
        <TextField
          label={t("ui.settings.add.placeholder_key", "KEY")}
          value={newKey}
          onChange={(event) => setNewKey(event.target.value)}
          fullWidth
        />
        <TextField
          label={t("ui.settings.add.placeholder_value", "Value")}
          value={newValue}
          onChange={(event) => setNewValue(event.target.value)}
          fullWidth
        />
        <Button variant="outlined" onClick={handleAdd}>
          {t("ui.actions.add", "Add")}
        </Button>
      </Stack>
      <Stack direction="row" spacing={2} alignItems="center" mt={3}>
        <Button variant="contained" onClick={handleSave}>
          {t("ui.settings.save_all", "Save All Settings")}
        </Button>
        <Typography variant="body2" color="success.main">
          {message}
        </Typography>
      </Stack>
    </Paper>
  );
}
