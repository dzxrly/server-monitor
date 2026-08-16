import { describe, expect, it } from 'vitest';

import { normalizeConfig } from '@/features/settings/model/config';

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
});
