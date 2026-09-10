import { describe, expect, it } from 'vitest';

import {
  normalizeConfig,
  partialConfigSchema,
} from '@/features/settings/model/config';

describe('config migration', () => {
  it('adds v1 defaults while preserving an old server list', () => {
    const config = normalizeConfig({
      darkMode: true,
      serverListConfig: [
        {
          customName: 'Local',
          uniqueId: 'legacy-id',
          serverUrl: 'http://127.0.0.1:6543',
          tagColor: '#123456',
          gpuServer: { gpuType: 'NVIDIA' },
        },
      ],
    });

    expect(config.darkMode).toBe(true);
    expect(config.processLimit).toBe(5);
    expect(config.serverListConfig[0]?.uniqueId).toBe('legacy-id');
  });

  it('rejects malformed persisted data', () => {
    const config = normalizeConfig({ refreshTimeSec: 0 });
    expect(config.refreshTimeSec).toBe(5);
    expect(config.serverListConfig).toEqual([]);
  });

  it.each(['PB', 'EB'])(
    'preserves %s memory and GPU units when importing or reloading configuration',
    (unit) => {
      const saved = {
        memoryUnit: unit,
        gpuMemoryUnit: unit,
        refreshTimeSec: 7,
        serverListConfig: [
          {
            customName: 'Existing server',
            uniqueId: 'existing-id',
            serverUrl: 'http://127.0.0.1:6543',
            tagColor: '#123456',
          },
        ],
      };

      expect(partialConfigSchema.safeParse(saved).success).toBe(true);
      expect(normalizeConfig(JSON.parse(JSON.stringify(saved)))).toMatchObject(
        saved,
      );
    },
  );
});
