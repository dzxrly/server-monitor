import { describe, expect, it } from 'vitest';

import { calculateMasonryRowSpan } from '@/features/monitoring/composables/use-masonry-grid';

describe('calculateMasonryRowSpan', () => {
  it('reserves one vertical gap after the card', () => {
    expect(calculateMasonryRowSpan(240.25, 1, 13.6)).toBe(254);
  });

  it('supports row units larger than one pixel', () => {
    expect(calculateMasonryRowSpan(240, 2, 14)).toBe(127);
  });

  it('returns a safe minimum for invalid measurements', () => {
    expect(calculateMasonryRowSpan(Number.NaN, 0, -10)).toBe(1);
  });
});
