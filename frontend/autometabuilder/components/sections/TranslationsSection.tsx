import { Button, Chip, Paper, Stack, TextField, Typography } from "@mui/material";
import useTranslationManager from "../../hooks/useTranslationManager";

type TranslationsSectionProps = {
  languages: Record<string, string>;
  onRefresh: () => void;
  t: (key: string, fallback?: string) => string;
  active: boolean;
};

export default function TranslationsSection({ languages, onRefresh, t, active }: TranslationsSectionProps) {
  const {
    selected,
    editorValue,
    message,
    error,
    newLang,
    setSelected,
    setEditorValue,
    setNewLang,
    handleSave,
    handleCreate,
    handleDelete,
  } = useTranslationManager({ languages, onRefresh, t });

  return (
    <Paper
      id="translations"
      className={active ? "active" : ""}
      sx={{ p: 3, mb: 3, backgroundColor: "var(--color-panel-bg)", display: active ? "block" : "none" }}
    >
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
              backgroundColor: "var(--color-input-bg)",
              borderRadius: 2,
              color: "var(--color-text-strong)",
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
