import "../autometabuilder/styles/globals.scss";

export const parameters = {
  layout: "fullscreen",
  backgrounds: {
    default: "dark",
    values: [
      { name: "dark", value: "#04070f" },
      { name: "panel", value: "#0d111b" },
    ],
  },
  actions: { argTypesRegex: "^on[A-Z].*" },
};
