import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    server: {
      proxy: {
        '/api': 'http://localhost:5000'
      }
    }
    build: {
        rollupOptions: {
            external: ['/env.js']
            }
        },
  plugins: [react()],
  resolve: {
    alias: {
        '@frontend': path.resolve(__dirname, 'src')
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts'
  }
})
