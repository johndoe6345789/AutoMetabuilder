import { ReactNode } from "react";
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
    <div className="app-shell">
      <Sidebar items={navItems} selected={section} onSelect={onSectionChange} t={t} />
      <div className="content-shell">
        <header className="content-shell__header">
          <h1>{t("ui.app.title", "AutoMetabuilder Dashboard")}</h1>
          <p>{t("ui.dashboard.subtitle", "Control the bot and monitor system activity")}</p>
        </header>
        <div className="content-shell__body">{children}</div>
      </div>
    </div>
  );
}
