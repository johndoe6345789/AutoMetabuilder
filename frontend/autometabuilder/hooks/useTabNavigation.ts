import { useState, useCallback } from "react";

export function useTabNavigation(initialTab = 0) {
  const [selectedTab, setSelectedTab] = useState(initialTab);

  const handleTabChange = useCallback((_: unknown, newValue: number) => {
    setSelectedTab(newValue);
  }, []);

  return { selectedTab, handleTabChange };
}
