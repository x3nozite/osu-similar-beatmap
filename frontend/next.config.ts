import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  turbopack: {
    root: __dirname,
  },
  images: {
    remotePatterns: [{ hostname: "assets.ppy.sh" }]
  },
  output: "standalone",
};

export default nextConfig;
