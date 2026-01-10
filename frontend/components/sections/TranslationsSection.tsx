import { FormEvent, useEffect, useState } from "react";
import {
  Button,
  Chip,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
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
    <Paper id="translations" sx={{ p: 3, mb: 3, backgroundColor: "#0d111b" }}>
      <Typography variant="h5" gutterBottom>
        {t("ui.translations.title", "Translations")}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {t("ui.translations.subtitle", "Create, edit, and maintain language files for bot messages")}
      </Typography>
      <Stack spacing={2} sx={{ mt: 2 }}>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          {Object.entries(languages).map(([lang, label]) => (
            <Chip
              label={`${lang} (${label})`}
              key={lang}
              variant={selected === lang ? "filled" : "outlined"}
              onClick={() => setSelected(lang)}
              clickable
            />
          ))}
        </Stack>
        <TextField
          multiline
          minRows={12}
          value={editorValue}
          onChange={(event) => setEditorValue(event.target.value)}
          InputProps={{
            sx: {
              backgroundColor: "#030712",
              borderRadius: 2,
              color: "white",
              fontFamily: "JetBrains Mono, monospace",
            },
          }}
        />
      </Stack>
      <Stack direction="row" spacing={2} mt={2}>
        <Button variant="contained" onClick={handleSave} disabled={!selected}>
          {t("ui.actions.save", "Save")}
        </Button>
        <Button variant="outlined" onClick={handleDelete} disabled={!selected}>
          {t("ui.actions.delete", "Delete")}
        </Button>
        <Stack component="form" onSubmit={handleCreate} direction="row" spacing={1} flex={1}>
          <TextField
            placeholder={t("ui.translations.add_language_placeholder", "Add language...")}
            value={newLang}
            onChange={(event) => setNewLang(event.target.value)}
            fullWidth
          />
          <Button type="submit" variant="contained">
            {t("ui.actions.add", "Add")}
          </Button>
        </Stack>
      </Stack>
      {(message || error) && (
        <Typography variant="body2" color={error ? "error.main" : "success.main"} mt={2}>
          {message || error}
        </Typography>
      )}
    </Paper>
  );
}
