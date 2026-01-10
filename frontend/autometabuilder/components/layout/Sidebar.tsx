import { Box, Divider, Drawer, List, ListItemButton, ListItemText, Typography } from "@mui/material";
import { NavigationItem } from "../../lib/types";

type SidebarProps = {
  items: NavigationItem[];
  selected: string;
  onSelect: (section: string) => void;
  t: (key: string, fallback?: string) => string;
};

export default function Sidebar({ items, selected, onSelect, t }: SidebarProps) {
  return (
    <Drawer variant="permanent" anchor="left" sx={{ width: 220, flexShrink: 0 }}>
      <Box sx={{ height: "100%", backgroundColor: "var(--color-sidebar-bg)" }}>
        <Box sx={{ px: 3, py: 2 }}>
          <Typography variant="overline" color="text.secondary">
            {t("ui.app.name", "AutoMetabuilder")}
          </Typography>
        </Box>
        <Divider sx={{ borderColor: "var(--color-divider)" }} />
        <List>
          {items.map((item) => (
            <ListItemButton
              key={item.section}
              selected={selected === item.section}
              onClick={() => onSelect(item.section)}
              data-section={item.section}
              sx={{
                color: selected === item.section ? "var(--color-text-strong)" : "var(--color-text-muted-strong)",
              }}
            >
              <ListItemText primary={t(item.label_key, item.default_label)} primaryTypographyProps={{ fontSize: 14 }} />
            </ListItemButton>
          ))}
        </List>
      </Box>
    </Drawer>
  );
}
