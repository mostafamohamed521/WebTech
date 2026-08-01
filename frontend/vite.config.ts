import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
  },
  build: {
    // Explicit vendor chunking: keeps the heavy 3D/chart libraries out
    // of both the main entry bundle AND out of unrelated route chunks,
    // so they're fetched once, cached, and only when actually needed.
    rollupOptions: {
      output: {
        manualChunks: {
          "three-vendor": ["three", "@react-three/fiber", "@react-three/drei"],
          "charts-vendor": ["recharts"],
          "motion-vendor": ["framer-motion", "gsap"],
        },
      },
    },
    chunkSizeWarningLimit: 700,
  },
});
