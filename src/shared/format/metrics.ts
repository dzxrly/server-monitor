import type { ByteUnit } from '@/features/settings/model/config';

const UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'] as const;

export function rounded(value: number | null | undefined, digits = 0): number {
  if (value == null || !Number.isFinite(value)) return 0;
  const multiplier = 10 ** digits;
  return Math.round(value * multiplier) / multiplier;
}

export function formatBytes(
  bytes: number | null | undefined,
  preferredUnit?: ByteUnit,
  maxAutoUnit: 'TB' | 'PB' | 'EB' = 'TB',
): string {
  if (bytes == null || !Number.isFinite(bytes)) return '—';
  let unitIndex = preferredUnit ? UNITS.indexOf(preferredUnit) : 0;
  if (!preferredUnit) {
    const maxUnitIndex = UNITS.indexOf(maxAutoUnit);
    while (
      Math.abs(bytes) >= 1024 ** (unitIndex + 1) &&
      unitIndex < maxUnitIndex
    ) {
      unitIndex += 1;
    }
  }
  const value = bytes / 1024 ** unitIndex;
  return `${new Intl.NumberFormat(undefined, { maximumFractionDigits: value >= 100 ? 0 : 2 }).format(value)} ${UNITS[unitIndex]}`;
}

export function formatRate(bytesPerSecond: number | null | undefined): string {
  return bytesPerSecond == null ? '—' : `${formatBytes(bytesPerSecond)}/s`;
}

export function formatCpuFrequency(
  megahertz: number | null | undefined,
): string {
  if (megahertz == null || !Number.isFinite(megahertz) || megahertz <= 0) {
    return '—';
  }
  if (megahertz >= 1000) return `${(megahertz / 1000).toFixed(2)} GHz`;
  return `${rounded(megahertz)} MHz`;
}

export function formatTemperature(
  celsius: number | null | undefined,
  fahrenheit: boolean,
): string {
  if (celsius == null) return '—';
  const value = fahrenheit ? (celsius * 9) / 5 + 32 : celsius;
  return `${rounded(value, 1)} °${fahrenheit ? 'F' : 'C'}`;
}

export function formatUptime(seconds: number | null | undefined): string {
  if (seconds == null) return '—';
  const days = Math.floor(seconds / 86_400);
  const hours = Math.floor((seconds % 86_400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return [days ? `${days}d` : '', hours ? `${hours}h` : '', `${minutes}m`]
    .filter(Boolean)
    .join(' ');
}

export function usageColor(
  value: number | null | undefined,
  freeThreshold: number,
  midThreshold: number,
): 'free-color' | 'mid-color' | 'max-color' {
  const resolved = value ?? 0;
  if (resolved < freeThreshold) return 'free-color';
  if (resolved < midThreshold) return 'mid-color';
  return 'max-color';
}
