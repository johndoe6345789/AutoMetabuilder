import { useState } from "react";
import { UIStatus } from "../../lib/types";

type DashboardSectionProps = {
  status: UIStatus;
  logs: string;
  onRun: (payload: { mode?: string; iterations?: number; yolo?: boolean; stop_at_mvp?: boolean }) => Promise<void>;
  t: (key: string, fallback?: string) => string;
};

export default function DashboardSection({ status, logs, onRun, t }: DashboardSectionProps) {
  const [mode, setMode] = useState("once");
  const [iterations, setIterations] = useState(1);
  const [stopAtMvp, setStopAtMvp] = useState(false);
  const [feedback, setFeedback] = useState("");

  const handleRun = async () => {
    const isYolo = mode === "yolo";
    setFeedback(t("ui.dashboard.status.bot_label", "Bot Status") + " — submitting");
    try {
      await onRun({ mode, iterations, yolo: isYolo, stop_at_mvp: stopAtMvp });
      setFeedback(t("ui.dashboard.start_bot", "Start Bot") + " " + t("ui.dashboard.status.running", "Running"));
    } catch (error) {
      console.error(error);
      setFeedback(t("ui.dashboard.status.idle", "Idle"));
    }
  };

  return (
    <section className="section-card" id="dashboard">
      <div className="section-card__header">
        <h2>{t("ui.dashboard.title", "Dashboard")}</h2>
        <p>{t("ui.dashboard.subtitle", "Control the bot and monitor system activity")}</p>
      </div>
      <div className="dashboard-grid">
        <div className="dashboard-panel">
          <h3>{t("ui.dashboard.bot_control", "Bot Control")}</h3>
          <div className="dashboard-panel__strategy">
            <label>
              <input type="radio" name="mode" value="once" checked={mode === "once"} onChange={() => setMode("once")} />
              <span>{t("ui.dashboard.run.single.title", "Single Iteration")}</span>
            </label>
            <label>
              <input type="radio" name="mode" value="iterations" checked={mode === "iterations"} onChange={() => setMode("iterations")} />
              <span>{t("ui.dashboard.run.repeat.title", "Repeat")}</span>
            </label>
            <label>
              <input type="radio" name="mode" value="yolo" checked={mode === "yolo"} onChange={() => setMode("yolo")} />
              <span>{t("ui.dashboard.run.yolo.title", "YOLO")}</span>
            </label>
          </div>
          {mode === "iterations" && (
            <label className="field-group">
              <span>{t("ui.dashboard.run.repeat.label", "Iterations")}</span>
              <input type="number" min={1} value={iterations} onChange={(event) => setIterations(Number(event.target.value) || 1)} />
            </label>
          )}
          <label className="field-group">
            <input type="checkbox" checked={stopAtMvp} onChange={(event) => setStopAtMvp(event.target.checked)} />
            <span>{t("ui.dashboard.stop_mvp.title", "Stop at MVP")}</span>
          </label>
          <button className="primary" type="button" onClick={handleRun} disabled={status.is_running}>
            {t("ui.dashboard.start_bot", "Start Bot")}
          </button>
          <p className="status-text">
            {status.is_running ? t("ui.dashboard.status.running", "Running") : t("ui.dashboard.status.idle", "Idle")} •{" "}
            {status.mvp_reached ? t("ui.dashboard.status.mvp_reached", "Reached") : t("ui.dashboard.status.mvp_progress", "In Progress")}
          </p>
          <p className="status-feedback">{feedback}</p>
        </div>
        <div className="dashboard-panel">
          <h3>{t("ui.dashboard.logs.title", "Recent Logs")}</h3>
          <pre className="log-output">{logs.slice(-1200) || t("ui.dashboard.status.idle", "Idle")}</pre>
        </div>
      </div>
    </section>
  );
}
