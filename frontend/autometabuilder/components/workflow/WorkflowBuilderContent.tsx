import { Box, Stack } from "@mui/material";
import { WorkflowGraph, WorkflowPluginMap } from "../../lib/types";
import WorkflowCanvas from "./WorkflowCanvas";
import WorkflowInspector from "./WorkflowInspector";
import WorkflowPalette from "./WorkflowPalette";

type WorkflowBuilderContentProps = {
  selectedTab: number;
  graph: WorkflowGraph;
  plugins: WorkflowPluginMap;
  t: (key: string, fallback?: string) => string;
};

export default function WorkflowBuilderContent({
  selectedTab,
  graph,
  plugins,
  t,
}: WorkflowBuilderContentProps) {
  return (
    <Stack direction="row" spacing={2}>
      <Box sx={{ flex: 1 }}>
        {selectedTab === 0 && <WorkflowCanvas graph={graph} plugins={plugins} t={t} />}
        {selectedTab === 1 && <WorkflowInspector t={t} />}
      </Box>
      <Box sx={{ width: 300 }}>
        <WorkflowPalette t={t} />
      </Box>
    </Stack>
  );
}
