import type { StorybookConfig } from "@storybook/nextjs";

const config: StorybookConfig = {
  stories: ["../autometabuilder/**/*.stories.@(tsx|mdx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
  ],
  framework: "@storybook/react-webpack5",
  docs: {
    autodocs: "tag",
  },
};

export default config;
