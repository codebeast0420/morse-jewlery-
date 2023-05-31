import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/static/",
  server: {
    host: "localhost",
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  build: {
    outDir: resolve("../static/prod"),
    assetsDir: "",
    manifest: true,
    emptyOutDir: true,
    target: "es2015",
    rollupOptions: {
      input: {
        mainjs: resolve("./src/main.js"),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
});
