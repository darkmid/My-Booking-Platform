import { fileURLToPath, URL } from "node:url";

import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load environment variables from .env files
  const env = loadEnv(mode, process.cwd());
  
  // Get backend API address
  const backendUrl = env.VITE_BACKEND_BASE || 'http://localhost:3000';
  console.log('Backend URL:', backendUrl);
  
  return {
    plugins: [vue(), vueJsx()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      port: 8080,
      proxy: {
        "/api/v1": {
          target: backendUrl,
          changeOrigin: true,
          rewrite: (path) => path,
        },
      },
    },
  };
});
