import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5188/PromptBook/',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'helium',
      use: { 
        ...devices['Desktop Chrome'],
        channel: 'chrome',
        launchOptions: {
          executablePath: '/Applications/Helium.app/Contents/MacOS/Helium'
        }
      },
    },
  ],
  webServer: {
    command: 'npm run dev -- --port 5188',
    url: 'http://localhost:5188/PromptBook/',
    reuseExistingServer: !process.env.CI,
  },
});
