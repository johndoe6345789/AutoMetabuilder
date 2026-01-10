import { useEffect, useState } from "react";
import { Box, Button, Paper, Stack, TextField, Typography } from "@mui/material";

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
    <Paper id="prompt" sx={{ p: 3, mb: 3, backgroundColor: "#0d111b" }}>
      <Typography variant="h5" gutterBottom>
        {t("ui.prompt.title", "Prompt Builder")}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {t("ui.prompt.subtitle", "Shape how the assistant thinks, speaks, and decides")}
      </Typography>
      <TextField
        multiline
        minRows={10}
        value={draft}
        onChange={(event) => setDraft(event.target.value)}
        fullWidth
        InputProps={{
          sx: {
            backgroundColor: "#030712",
            borderRadius: 2,
            color: "white",
            fontFamily: "JetBrains Mono, monospace",
          },
        }}
      />
      <Stack direction="row" spacing={2} alignItems="center" mt={2}>
        <Button variant="contained" onClick={handleSave}>
          {t("ui.prompt.save", "Save Prompt")}
        </Button>
        <Typography variant="body2" color="success.main">
          {message}
        </Typography>
      </Stack>
    </Paper>
  );
}
