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
      <Box sx={{ height: "100%", backgroundColor: "#0f172a" }}>
        <Box sx={{ px: 3, py: 2 }}>
          <Typography variant="overline" color="text.secondary">
            {t("ui.app.name", "AutoMetabuilder")}
          </Typography>
        </Box>
        <Divider sx={{ borderColor: "rgba(255,255,255,0.08)" }} />
        <List>
          {items.map((item) => (
            <ListItemButton
              key={item.section}
              selected={selected === item.section}
              onClick={() => onSelect(item.section)}
              data-section={item.section}
              sx={{
                color: selected === item.section ? "#fff" : "rgba(226,232,240,0.8)",
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
