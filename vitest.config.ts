import { getTestingConfig } from '@quasar/app-vite/testing';

import { defineConfig, mergeConfig } from 'vitest/config';

export default defineConfig(async () =>
  mergeConfig(await getTestingConfig(), {
    test: {
      environment: 'jsdom',
      include: ['src/**/*.test.ts'],
    },
  }),
);
