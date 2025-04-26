import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'url'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './setupTests.ts'
  },
  resolve: {
      alias: {
        '@frontend': fileURLToPath(new URL('./src', import.meta.url))
      }
  }
})
