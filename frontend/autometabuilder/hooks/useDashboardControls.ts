import { useCallback, useState } from "react";

export type DashboardRunPayload = {
  mode?: string;
  iterations?: number;
  yolo?: boolean;
  stop_at_mvp?: boolean;
};

type UseDashboardControlsArgs = {
  onRun: (payload: DashboardRunPayload) => Promise<void>;
  t: (key: string, fallback?: string) => string;
};

type UseDashboardControlsResult = {
  mode: string;
  setMode: (next: string) => void;
  iterations: number;
  setIterations: (next: number) => void;
  stopAtMvp: boolean;
  setStopAtMvp: (next: boolean) => void;
  feedback: string;
  handleRun: () => Promise<void>;
};

export default function useDashboardControls({ onRun, t }: UseDashboardControlsArgs): UseDashboardControlsResult {
  const [mode, setMode] = useState("once");
  const [iterations, setIterations] = useState(1);
  const [stopAtMvp, setStopAtMvp] = useState(false);
  const [feedback, setFeedback] = useState("");

  const handleRun = useCallback(async () => {
    const isYolo = mode === "yolo";
    setFeedback(`${t("ui.dashboard.status.bot_label", "Bot Status")} — submitting`);
    try {
      await onRun({ mode, iterations, yolo: isYolo, stop_at_mvp: stopAtMvp });
      setFeedback(`${t("ui.dashboard.start_bot", "Start Bot")} ${t("ui.dashboard.status.running", "Running")}`);
    } catch (error) {
      console.error(error);
      setFeedback(t("ui.dashboard.status.idle", "Idle"));
    }
  }, [iterations, mode, onRun, stopAtMvp, t]);

  return {
    mode,
    setMode,
    iterations,
    setIterations,
    stopAtMvp,
    setStopAtMvp,
    feedback,
    handleRun,
  };
}
