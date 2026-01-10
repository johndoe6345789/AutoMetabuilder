import { NavigationItem } from "../../lib/types";

type SidebarProps = {
  items: NavigationItem[];
  selected: string;
  onSelect: (section: string) => void;
  t: (key: string, fallback?: string) => string;
};

export default function Sidebar({ items, selected, onSelect, t }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <span>{t("ui.app.name", "AutoMetabuilder")}</span>
      </div>
      <nav>
        {items.map((item) => (
          <button
            key={item.section}
            type="button"
            className={`sidebar__item ${selected === item.section ? "active" : ""}`}
            onClick={() => onSelect(item.section)}
            data-section={item.section}
          >
            <span>{t(item.label_key, item.default_label)}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
