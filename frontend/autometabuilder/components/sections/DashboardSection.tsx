import {
  Box,
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  Paper,
  Radio,
  RadioGroup,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { UIStatus } from "../../lib/types";
import useDashboardControls, { DashboardRunPayload } from "../../hooks/useDashboardControls";

type DashboardSectionProps = {
  status: UIStatus;
  logs: string;
  onRun: (payload: DashboardRunPayload) => Promise<void>;
  t: (key: string, fallback?: string) => string;
};

export default function DashboardSection({ status, logs, onRun, t }: DashboardSectionProps) {
  const { mode, setMode, iterations, setIterations, stopAtMvp, setStopAtMvp, feedback, handleRun } = useDashboardControls({
    onRun,
    t,
  });

  return (
    <Paper id="dashboard" sx={{ p: 3, mb: 3, backgroundColor: "var(--color-panel-bg)" }}>
      <Typography variant="h5" gutterBottom>
        {t("ui.dashboard.title", "Dashboard")}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {t("ui.dashboard.subtitle", "Control the bot and monitor system activity")}
      </Typography>
      <Stack direction={{ xs: "column", md: "row" }} spacing={3} mt={2}>
        <Paper sx={{ flex: 1, p: 2, backgroundColor: "var(--color-panel-alt)" }}>
          <Typography variant="subtitle1" gutterBottom>
            {t("ui.dashboard.bot_control", "Bot Control")}
          </Typography>
          <FormControl component="fieldset">
            <RadioGroup row value={mode} onChange={(event) => setMode(event.target.value)} name="run-mode">
              {["once", "iterations", "yolo"].map((value) => (
                <FormControlLabel
                  key={value}
                  value={value}
                  control={<Radio size="small" />}
                  label={t(`ui.dashboard.run.${value}.title`, value === "iterations" ? "Repeat" : value.charAt(0).toUpperCase() + value.slice(1))}
                />
              ))}
            </RadioGroup>
          </FormControl>
          {mode === "iterations" && (
            <TextField
              type="number"
              size="small"
              label={t("ui.dashboard.run.repeat.label", "Iterations")}
              value={iterations}
              onChange={(event) => setIterations(Number(event.target.value) || 1)}
              sx={{ mt: 1, width: 140 }}
            />
          )}
          <FormControlLabel
            control={<Checkbox checked={stopAtMvp} onChange={(event) => setStopAtMvp(event.target.checked)} />}
            label={t("ui.dashboard.stop_mvp.title", "Stop at MVP")}
            sx={{ mt: 1 }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleRun}
            disabled={status.is_running}
            sx={{ mt: 2 }}
          >
            {t("ui.dashboard.start_bot", "Start Bot")}
          </Button>
          <Typography variant="caption" color="text.secondary" display="block" mt={1}>
            {status.is_running ? t("ui.dashboard.status.running", "Running") : t("ui.dashboard.status.idle", "Idle")} •
            {" "}
            {status.mvp_reached ? t("ui.dashboard.status.mvp_reached", "Reached") : t("ui.dashboard.status.mvp_progress", "In Progress")}
          </Typography>
          <Typography variant="caption" color="primary">
            {feedback}
          </Typography>
        </Paper>
        <Paper sx={{ flex: 1, p: 2, backgroundColor: "var(--color-panel-alt)" }}>
          <Typography variant="subtitle1" gutterBottom>
            {t("ui.dashboard.logs.title", "Recent Logs")}
          </Typography>
          <Box component="pre" sx={{ maxHeight: 240, overflow: "auto", fontSize: 12, color: "var(--color-text-strong)" }}>
            {logs.slice(-1200) || t("ui.dashboard.status.idle", "Idle")}
          </Box>
        </Paper>
      </Stack>
    </Paper>
  );
}
