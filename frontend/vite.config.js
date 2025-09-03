import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Configuration Vite pour React
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // port de dev local
  },
});
