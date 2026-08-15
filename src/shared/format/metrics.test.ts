import { describe, expect, it } from 'vitest';

import {
  formatBytes,
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

  it('converts Celsius to Fahrenheit only in the UI', () => {
    expect(formatTemperature(50, false)).toBe('50 °C');
    expect(formatTemperature(50, true)).toBe('122 °F');
  });

  it('uses the configured usage thresholds', () => {
    expect(usageColor(10, 30, 70)).toBe('free-color');
    expect(usageColor(50, 30, 70)).toBe('mid-color');
    expect(usageColor(90, 30, 70)).toBe('max-color');
  });
});
