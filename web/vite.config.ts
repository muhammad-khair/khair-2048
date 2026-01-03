import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react() as any],
  test: {
    environment: 'happy-dom',
    globals: true,
    setupFiles: path.resolve(__dirname, './test/setup.ts'),
    include: [path.resolve(__dirname, './test/**/*.{test,spec}.tsx')],
  },
})
