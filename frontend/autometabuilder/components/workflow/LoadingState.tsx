import { Paper, Typography } from "@mui/material";

type LoadingStateProps = {
  message: string;
};

export default function LoadingState({ message }: LoadingStateProps) {
  return (
    <Paper sx={{ p: 3, backgroundColor: "var(--color-panel-bg)" }}>
      <Typography variant="body2" color="text.secondary">
        {message}
      </Typography>
    </Paper>
  );
}
