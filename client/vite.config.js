import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    extensions: [".mjs", ".cjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
    alias: {
      "@": path.resolve(__dirname, "./src")
    }
  },
  preview: {
    port: 8090
  },
  server: {
    port: 8090
  },
  build: {
    outDir: 'dist', // Main output directory
    rollupOptions: {
      output: {
        assetFileNames: ({name}) => {
          if (/\.css$/.test(name ?? '')) {
            return 'static/css/[name]-[hash][extname]';
          } else if (/\.(png|jpe?g|gif|svg)$/.test(name ?? '')) {
            return 'static/images/[name]-[hash][extname]';
          }
          return 'static/assets/[name]-[hash][extname]';
        },
        chunkFileNames: 'static/js/[name]-[hash].js',
        entryFileNames: 'static/js/[name]-[hash].js',
      }
    }
  }
})
