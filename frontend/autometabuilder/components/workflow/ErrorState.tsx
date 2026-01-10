import { Paper, Typography } from "@mui/material";

type ErrorStateProps = {
  message: string;
};

export default function ErrorState({ message }: ErrorStateProps) {
  return (
    <Paper sx={{ p: 3, backgroundColor: "var(--color-panel-bg)" }}>
      <Typography color="error">{message}</Typography>
    </Paper>
  );
}
