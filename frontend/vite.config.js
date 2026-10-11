import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react({
    plugins: []
  })],
  server: {
    port: 3000,
    hmr: false,
    proxy: {
      '/api/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/api/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})