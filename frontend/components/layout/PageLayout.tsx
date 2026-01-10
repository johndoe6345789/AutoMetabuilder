import { ReactNode } from "react";
import { Box, Toolbar, Typography } from "@mui/material";
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
  return (
    <Box sx={{ display: "flex" }}>
      <Sidebar items={navItems} selected={section} onSelect={onSectionChange} t={t} />
      <Box component="main" sx={{ flexGrow: 1, p: 3, bgcolor: "#04070f", minHeight: "100vh" }}>
        <Toolbar disableGutters>
          <div>
            <Typography variant="h4" color="text.primary" gutterBottom>
              {t("ui.app.title", "AutoMetabuilder Dashboard")}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {t("ui.dashboard.subtitle", "Control the bot and monitor system activity")}
            </Typography>
          </div>
        </Toolbar>
        <Box>{children}</Box>
      </Box>
    </Box>
  );
}
