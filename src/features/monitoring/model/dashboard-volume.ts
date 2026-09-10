import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';

type StorageVolume = MetricsSnapshot['storage']['volumes'][number];

export function selectDashboardVolume(
  volumes: readonly StorageVolume[],
): StorageVolume | undefined {
  const primary = volumes.find(
    (volume) =>
      volume.mountpoint === '/' || /^c:[\\/]?$/i.test(volume.mountpoint),
  );
  return (
    primary ??
    volumes.reduce<StorageVolume | undefined>(
      (highest, volume) =>
        !highest || volume.usagePercent > highest.usagePercent
          ? volume
          : highest,
      undefined,
    )
  );
}
