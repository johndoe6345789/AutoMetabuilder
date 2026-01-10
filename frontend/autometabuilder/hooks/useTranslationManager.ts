import { FormEvent, useCallback, useEffect, useState } from "react";
import { createTranslation, deleteTranslation, fetchTranslation, updateTranslation } from "../lib/api";

type UseTranslationManagerArgs = {
  languages: Record<string, string>;
  onRefresh: () => void;
  t: (key: string, fallback?: string) => string;
};

type UseTranslationManagerResult = {
  selected: string | null;
  editorValue: string;
  message: string;
  error: string;
  newLang: string;
  setSelected: (lang: string) => void;
  setEditorValue: (next: string) => void;
  setNewLang: (next: string) => void;
  handleSave: () => Promise<void>;
  handleCreate: (event: FormEvent) => Promise<void>;
  handleDelete: () => Promise<void>;
};

export default function useTranslationManager({ languages, onRefresh, t }: UseTranslationManagerArgs): UseTranslationManagerResult {
  const [selected, setSelected] = useState<string | null>(null);
  const [editorValue, setEditorValue] = useState("{}");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [newLang, setNewLang] = useState("");

  const loadContent = useCallback(async (lang: string) => {
    setError("");
    const data = await fetchTranslation(lang);
    setEditorValue(JSON.stringify(data.content, null, 2));
  }, []);

  useEffect(() => {
    if (!selected && Object.keys(languages).length) {
      setSelected(Object.keys(languages)[0]);
    }
  }, [languages, selected]);

  useEffect(() => {
    if (selected) {
      void loadContent(selected);
    }
  }, [loadContent, selected]);

  const handleSave = useCallback(async () => {
    if (!selected) return;
    try {
      const payload = JSON.parse(editorValue);
      await updateTranslation(selected, payload);
      setMessage(t("ui.translations.notice.saved", "Translation saved!"));
      onRefresh();
    } catch (err) {
      setError(String(err));
    }
  }, [editorValue, onRefresh, selected, t]);

  const handleCreate = useCallback(
    async (event: FormEvent) => {
      event.preventDefault();
      if (!newLang.trim()) return;
      await createTranslation(newLang.trim());
      setNewLang("");
      onRefresh();
    },
    [newLang, onRefresh]
  );

  const handleDelete = useCallback(async () => {
    if (!selected) return;
    await deleteTranslation(selected);
    setSelected(null);
    onRefresh();
  }, [onRefresh, selected]);

  return {
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
  };
}
