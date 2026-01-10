import { Chip, IconButton, Stack } from "@mui/material";
import SettingsIcon from "@mui/icons-material/Settings";

type NodeHeaderProps = {
  type: string;
  onSettings?: () => void;
};

export default function NodeHeader({ type, onSettings }: NodeHeaderProps) {
  return (
    <Stack direction="row" alignItems="center" justifyContent="space-between">
      <Chip
        label={type}
        size="small"
        sx={{
          fontSize: "0.7rem",
          height: 20,
          backgroundColor: "var(--color-accent)",
        }}
      />
      <IconButton size="small" sx={{ p: 0.5 }} onClick={onSettings}>
        <SettingsIcon fontSize="small" />
      </IconButton>
    </Stack>
  );
}
