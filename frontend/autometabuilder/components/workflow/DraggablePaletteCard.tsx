"use client";

import { DragEvent } from "react";
import { Box, Chip, Paper, Stack, Tooltip, Typography } from "@mui/material";
import { WorkflowPluginDefinition } from "../../lib/types";

type DraggablePaletteCardProps = {
  id: string;
  plugin: WorkflowPluginDefinition;
  t: (key: string, fallback?: string) => string;
};

export default function DraggablePaletteCard({ id, plugin, t }: DraggablePaletteCardProps) {
  const onDragStart = (event: DragEvent<HTMLDivElement>) => {
    event.dataTransfer.setData("application/reactflow", id);
    event.dataTransfer.effectAllowed = "move";
  };

  const label = plugin.label ? t(plugin.label, id) : id;
  const description = plugin.description ? t(plugin.description, "") : "";
  const tags = plugin.tags || [];
  const category = plugin.category || "general";

  return (
    <Tooltip title={description || label} arrow placement="right">
      <Paper
        draggable
        onDragStart={onDragStart}
        sx={{
          p: 1.5,
          cursor: "grab",
          transition: "all 0.2s",
          "&:hover": {
            boxShadow: 4,
            backgroundColor: "var(--color-hover-bg)",
          },
          "&:active": {
            cursor: "grabbing",
          },
        }}
      >
        <Stack spacing={0.5}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <Chip
              label={category}
              size="small"
              sx={{
                fontSize: "0.65rem",
                height: 18,
                backgroundColor: "var(--color-accent)",
              }}
            />
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              {label}
            </Typography>
          </Stack>

          {description && (
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {description}
            </Typography>
          )}

          {tags.length > 0 && (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {tags.slice(0, 3).map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  size="small"
                  variant="outlined"
                  sx={{
                    fontSize: "0.6rem",
                    height: 16,
                  }}
                />
              ))}
              {tags.length > 3 && (
                <Typography variant="caption" color="text.secondary">
                  +{tags.length - 3}
                </Typography>
              )}
            </Box>
          )}
        </Stack>
      </Paper>
    </Tooltip>
  );
}
