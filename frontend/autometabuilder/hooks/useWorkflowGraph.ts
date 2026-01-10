import { useEffect, useState } from "react";
import { fetchWorkflowGraph } from "../lib/api";
import { WorkflowGraph } from "../lib/types";

export function useWorkflowGraph() {
  const [graph, setGraph] = useState<WorkflowGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    let alive = true;
    setLoading(true);

    fetchWorkflowGraph()
      .then((data) => {
        if (alive) {
          setGraph(data);
          setError("");
        }
      })
      .catch((err) => {
        if (alive) {
          setError(String(err));
        }
      })
      .finally(() => {
        if (alive) {
          setLoading(false);
        }
      });

    return () => {
      alive = false;
    };
  }, []);

  return { graph, loading, error };
}
