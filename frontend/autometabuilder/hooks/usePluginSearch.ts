import { useMemo, useState } from "react";
import { WorkflowPluginMap } from "../lib/types";

export function usePluginSearch(plugins: WorkflowPluginMap, t: (key: string, fallback?: string) => string) {
  const [search, setSearch] = useState("");

  const filteredPlugins = useMemo(() => {
    const query = search.trim().toLowerCase();
    return Object.entries(plugins).filter(([id, plugin]) => {
      const label = plugin.label ? t(plugin.label, id) : id;
      const category = plugin.category || "";
      const tags = (plugin.tags || []).join(" ");
      const searchText = `${id} ${label} ${category} ${tags}`.toLowerCase();
      return !query || searchText.includes(query);
    });
  }, [plugins, search, t]);

  return { search, setSearch, filteredPlugins };
}
