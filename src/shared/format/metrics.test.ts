import { describe, expect, it } from 'vitest';

import {
  formatBytes,
  formatCpuFrequency,
  formatRate,
  formatTemperature,
  usageColor,
} from '@/shared/format/metrics';

describe('metric formatters', () => {
  it('formats byte values and rates', () => {
    expect(formatBytes(1024)).toBe('1 KB');
    expect(formatBytes(1024 ** 3, 'GB')).toBe('1 GB');
    expect(formatRate(2048)).toBe('2 KB/s');
  });

  it('supports automatic disk capacity units through EB when requested', () => {
    expect(formatBytes(128 * 1024, undefined, 'EB')).toBe('128 KB');
    expect(formatBytes(1024 ** 5, undefined, 'EB')).toBe('1 PB');
    expect(formatBytes(1024 ** 6, undefined, 'EB')).toBe('1 EB');
    expect(formatBytes(1.5 * 1024 ** 6, undefined, 'EB')).toBe('1.5 EB');
    expect(formatBytes(1024 ** 7, undefined, 'EB')).toMatch(/ EB$/);
    expect(formatBytes(0, undefined, 'EB')).toBe('0 B');
    expect(formatBytes(null, undefined, 'EB')).toBe('—');
  });

  it('preserves default automatic limits and explicitly configured units', () => {
    expect(formatBytes(1024 ** 5)).toMatch(/ TB$/);
    expect(formatRate(1024 ** 5)).toMatch(/ TB\/s$/);
    expect(formatBytes(128 * 1024, 'GB', 'EB')).toBe('0 GB');
    expect(formatBytes(1024 ** 5, 'PB')).toBe('1 PB');
    expect(formatBytes(1.5 * 1024 ** 6, 'EB')).toBe('1.5 EB');
  });

  it('converts Celsius to Fahrenheit only in the UI', () => {
    expect(formatTemperature(50, false)).toBe('50 °C');
    expect(formatTemperature(50, true)).toBe('122 °F');
  });

  it('formats CPU frequency for compact readouts', () => {
    expect(formatCpuFrequency(3200)).toBe('3.20 GHz');
    expect(formatCpuFrequency(800)).toBe('800 MHz');
    expect(formatCpuFrequency(null)).toBe('—');
  });

  it('uses the configured usage thresholds', () => {
    expect(usageColor(10, 30, 70)).toBe('free-color');
    expect(usageColor(50, 30, 70)).toBe('mid-color');
    expect(usageColor(90, 30, 70)).toBe('max-color');
  });
});
