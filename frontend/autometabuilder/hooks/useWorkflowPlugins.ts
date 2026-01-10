import { useEffect, useState } from "react";
import { fetchWorkflowPlugins } from "../lib/api";
import { WorkflowPluginMap } from "../lib/types";

export function useWorkflowPlugins() {
  const [plugins, setPlugins] = useState<WorkflowPluginMap>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    let alive = true;
    setLoading(true);

    fetchWorkflowPlugins()
      .then((data) => {
        if (alive) {
          setPlugins(data);
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

  return { plugins, loading, error };
}
