import { describe, expect, it } from 'vitest';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import { mergeProcessRows } from '@/features/monitoring/model/process-rows';

describe('mergeProcessRows', () => {
  it('deduplicates resource rankings and defaults to descending CPU usage', () => {
    const processes: MetricsSnapshot['processes'] = {
      available: true,
      limit: 2,
      cpu: [
        {
          pid: 10,
          name: 'cpu.exe',
          cpuUsagePercent: 45,
          memoryBytes: 100,
          memoryUsagePercent: 1,
        },
        {
          pid: 20,
          name: 'shared.exe',
          cpuUsagePercent: 20,
          memoryBytes: 200,
          memoryUsagePercent: 2,
        },
      ],
      memory: [
        {
          pid: 30,
          name: 'memory.exe',
          cpuUsagePercent: 5,
          memoryBytes: 900,
          memoryUsagePercent: 9,
        },
        {
          pid: 20,
          name: 'shared.exe',
          cpuUsagePercent: 20,
          memoryBytes: 200,
          memoryUsagePercent: 2,
        },
      ],
      gpu: [
        {
          pid: 20,
          name: 'shared.exe',
          gpuUsagePercent: 60,
          gpuMemoryBytes: 4096,
        },
        {
          pid: 40,
          name: 'gpu.exe',
          gpuUsagePercent: 30,
          gpuMemoryBytes: 2048,
        },
      ],
    };

    const rows = mergeProcessRows(processes);

    expect(rows.map((row) => row.pid)).toEqual([10, 20, 30, 40]);
    expect(rows.find((row) => row.pid === 20)).toMatchObject({
      cpuUsagePercent: 20,
      memoryBytes: 200,
      gpuUsagePercent: 60,
      gpuMemoryBytes: 4096,
    });
  });
});
