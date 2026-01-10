import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  experimental: {
    appDir: "autometabuilder/app",
  },
};

export default nextConfig;
