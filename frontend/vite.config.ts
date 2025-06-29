import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import svgr from 'vite-plugin-svgr';
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    svgr(),
  ],
  root: '.',                    // если запускаешь из frontend/
  base: '/',                    // важно: относительные пути, т.к. WebApp работает по URL
  build: {
    outDir: 'dist',             // сюда соберется проект
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})