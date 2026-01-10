import { useEffect, useState } from "react";
import { Box, Chip, Divider, Paper, Stack, Typography } from "@mui/material";
import { fetchWorkflowGraph } from "../../lib/api";
import { WorkflowGraph } from "../../lib/types";

type WorkflowGraphPanelProps = {
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowGraphPanel({ t }: WorkflowGraphPanelProps) {
  const [graph, setGraph] = useState<WorkflowGraph | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let alive = true;
    void fetchWorkflowGraph()
      .then((payload) => {
        if (alive) {
          setGraph(payload);
        }
      })
      .catch((err) => {
        if (alive) {
          setError(String(err));
        }
      });
    return () => {
      alive = false;
    };
  }, []);

  return (
    <Paper sx={{ p: 2, backgroundColor: "#0b1221" }}>
      <Typography variant="subtitle1" gutterBottom>
        {t("ui.workflow.graph.title", "Workflow Graph")}
      </Typography>
      <Typography variant="caption" color="text.secondary" gutterBottom>
        {graph
          ? t("ui.workflow.graph.summary", "Nodes: {nodes}, Edges: {edges}")
              .replace("{nodes}", String(graph.count.nodes))
              .replace("{edges}", String(graph.count.edges))
          : t("ui.workflow.graph.loading", "Loading graph…")}
      </Typography>
      {error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <>
          <Stack spacing={1} divider={<Divider light sx={{ borderColor: "rgba(255,255,255,0.08)" }} />}>
            {graph?.nodes.map((node) => (
              <Box key={node.id} sx={{ display: "flex", flexDirection: "column" }}>
                <Stack direction="row" alignItems="center" spacing={1}>
                  <Chip size="small" label={node.type} />
                  <Typography variant="body2" color="text.secondary">
                    {node.label_key ? t(node.label_key, node.type) : node.type}
                  </Typography>
                </Stack>
                <Typography variant="caption" color="text.secondary">
                  {node.parent ? `${t("ui.workflow.graph.child_of", "child of")} ${node.parent}` : t("ui.workflow.graph.top_level", "top level")}
                </Typography>
              </Box>
            ))}
          </Stack>
          <Divider sx={{ my: 2, borderColor: "rgba(255,255,255,0.08)" }} />
          <Stack spacing={1}>
            {graph?.edges.map((edge, index) => (
              <Typography key={`${edge.from}-${edge.to}-${edge.var}-${index}`} variant="caption" color="text.secondary">
                {t("ui.workflow.graph.edge", "{from} → {to} ({var})")
                  .replace("{from}", edge.from)
                  .replace("{to}", edge.to)
                  .replace("{var}", edge.var)}
              </Typography>
            ))}
          </Stack>
        </>
      )}
    </Paper>
  );
}
