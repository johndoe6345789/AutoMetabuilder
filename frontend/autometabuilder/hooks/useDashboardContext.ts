import { useEffect, useMemo, useState } from "react";
import { fetchContext } from "../lib/api";
import { UIContext } from "../lib/types";

export default function useDashboardContext() {
  const [context, setContext] = useState<UIContext | null>(null);
  const [selectedSection, setSelectedSection] = useState("dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [snack, setSnack] = useState("");
  const [snackOpen, setSnackOpen] = useState(false);

  const loadContext = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchContext();
      setContext(data);
      setSelectedSection((prev) => prev || data.navigation[0]?.section || "dashboard");
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  };

  const ready = context !== null;
  const t = useMemo(
    () => (key: string, fallback?: string) => (context?.messages[key] ?? fallback ?? key),
    [context]
  );

  return {
    context,
    selectedSection,
    setSelectedSection,
    loading,
    error,
    snack,
    setSnack,
    snackOpen,
    setSnackOpen,
    loadContext,
    t,
    ready,
  };
}
