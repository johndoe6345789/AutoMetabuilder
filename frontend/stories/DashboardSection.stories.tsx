import type { Meta, StoryObj } from "@storybook/react";
import DashboardSection from "../autometabuilder/components/sections/DashboardSection";

const meta: Meta<typeof DashboardSection> = {
  title: "Sections/Dashboard",
  component: DashboardSection,
};

export default meta;

type Story = StoryObj<typeof DashboardSection>;

export const Default: Story = {
  args: {
    status: {
      is_running: false,
      mvp_reached: false,
      config: {},
    },
    logs: "Start: nothing happening yet.",
    onRun: async () => {},
    t: (key: string, fallback?: string) => fallback ?? key,
  },
};
