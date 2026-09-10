import { describe, expect, it } from 'vitest';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import { selectDashboardVolume } from '@/features/monitoring/model/dashboard-volume';

function volume(
  mountpoint: string,
  usagePercent: number,
): MetricsSnapshot['storage']['volumes'][number] {
  return {
    device: mountpoint,
    mountpoint,
    fileSystem: null,
    options: [],
    readOnly: false,
    totalBytes: 100,
    usedBytes: usagePercent,
    freeBytes: 100 - usagePercent,
    usagePercent,
  };
}

describe('selectDashboardVolume', () => {
  it('shows the Linux root instead of a full snap mount or data volume', () => {
    const root = volume('/', 23);
    const snap = { ...volume('/snap/bare/5', 100), readOnly: true };
    expect(selectDashboardVolume([snap, volume('/data', 85), root])).toBe(root);
  });

  it.each(['C:\\', 'C:/', 'c:\\', 'c:/', 'C:'])(
    'shows Windows drive %s instead of a fuller drive or mounted folder',
    (mountpoint) => {
      const system = volume(mountpoint, 0);
      expect(
        selectDashboardVolume([
          volume('D:\\', 99),
          volume('C:\\data', 80),
          system,
        ]),
      ).toBe(system);
    },
  );

  it('keeps the fullest-volume fallback when no system volume is reported', () => {
    const data = volume('/data', 75);
    const volumes = [volume('/home', 30), data];
    expect(selectDashboardVolume(volumes)).toBe(data);
    expect(volumes.map((item) => item.mountpoint)).toEqual(['/home', '/data']);
  });

  it('does not mistake a Windows mounted folder for the C drive root', () => {
    const data = volume('D:\\', 90);
    expect(selectDashboardVolume([volume('C:\\data', 20), data])).toBe(data);
  });

  it('returns no volume when storage data is empty', () => {
    expect(selectDashboardVolume([])).toBeUndefined();
  });
});
