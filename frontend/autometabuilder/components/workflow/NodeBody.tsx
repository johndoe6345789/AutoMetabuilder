import { Stack, Typography } from "@mui/material";

type NodeBodyProps = {
  label: string;
  category?: string;
  inputCount: number;
  outputCount: number;
  t: (key: string, fallback?: string) => string;
};

export default function NodeBody({ label, category, inputCount, outputCount, t }: NodeBodyProps) {
  return (
    <Stack spacing={0.5}>
      <Typography
        variant="body2"
        sx={{
          fontWeight: 500,
          color: "var(--color-text-strong)",
        }}
      >
        {label}
      </Typography>

      {category && (
        <Typography variant="caption" color="text.secondary">
          {t(`ui.workflow.category.${category}`, category)}
        </Typography>
      )}

      <Stack direction="row" spacing={1}>
        {inputCount > 0 && (
          <Typography variant="caption" color="text.secondary">
            {t("ui.workflow.node.inputs", "In: {count}").replace("{count}", String(inputCount))}
          </Typography>
        )}
        {outputCount > 0 && (
          <Typography variant="caption" color="text.secondary">
            {t("ui.workflow.node.outputs", "Out: {count}").replace("{count}", String(outputCount))}
          </Typography>
        )}
      </Stack>
    </Stack>
  );
}
