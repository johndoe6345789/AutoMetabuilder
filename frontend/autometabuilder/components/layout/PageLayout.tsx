"use client";

import { ReactNode, useEffect, useState } from "react";
import { Box, IconButton, Toolbar, Typography } from "@mui/material";
import { NavigationItem } from "../../lib/types";
import Sidebar from "./Sidebar";

type PageLayoutProps = {
  navItems: NavigationItem[];
  section: string;
  onSectionChange: (section: string) => void;
  t: (key: string, fallback?: string) => string;
  children: ReactNode;
};

export default function PageLayout({ navItems, section, onSectionChange, t, children }: PageLayoutProps) {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const initialTheme = document.documentElement.getAttribute("data-theme");
    if (initialTheme === "dark") {
      setTheme("dark");
    }
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const handleToggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <Box sx={{ display: "flex" }}>
      <Sidebar items={navItems} selected={section} onSelect={onSectionChange} t={t} />
      <Box component="main" sx={{ flexGrow: 1, p: 3, bgcolor: "var(--color-app-bg)", minHeight: "100vh" }}>
        <Toolbar disableGutters sx={{ justifyContent: "space-between" }}>
          <div>
            <Typography variant="h4" color="text.primary" gutterBottom>
              {t("ui.app.title", "AutoMetabuilder Dashboard")}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {t("ui.dashboard.subtitle", "Control the bot and monitor system activity")}
            </Typography>
          </div>
          <IconButton aria-label="Toggle theme" data-theme-toggle onClick={handleToggleTheme}>
            {theme === "light" ? "🌞" : "🌙"}
          </IconButton>
        </Toolbar>
        <Box>{children}</Box>
      </Box>
    </Box>
  );
}
