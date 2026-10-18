<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type {
  MemorySegment,
  MemorySegmentKey,
  MetricsSnapshot,
} from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import SegmentedRing from '@/features/monitoring/components/shared/SegmentedRing.vue';
import type {
  ByteUnit,
  MemoryColorMode,
} from '@/features/settings/model/config';
import { formatBytes, rounded, usageColor } from '@/shared/format/metrics';

const props = defineProps<{
  memory: MetricsSnapshot['memory'];
  unit: ByteUnit;
  colorMode: MemoryColorMode;
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();

// Same slot for the same role on each platform: what programs hold, what is
// waiting to be written back, what the kernel can reclaim, and what is empty.
// Slot 0 is free memory and always uses the ring track color.
const SEGMENT_STYLE: Record<MemorySegmentKey, { slot: number; label: string }> =
  {
    used: { slot: 1, label: 'memorySegmentUsed' },
    inUse: { slot: 1, label: 'memorySegmentInUse' },
    buffers: { slot: 2, label: 'memorySegmentBuffers' },
    modified: { slot: 2, label: 'memorySegmentModified' },
    cache: { slot: 3, label: 'memorySegmentCache' },
    standby: { slot: 3, label: 'memorySegmentStandby' },
    free: { slot: 0, label: 'memorySegmentFree' },
  };

function segmentColor(key: MemorySegmentKey): string {
  const { slot } = SEGMENT_STYLE[key];
  if (slot === 0) return 'var(--progress-track-color)';
  const palette = props.colorMode === 'highContrast' ? 'high' : 'low';
  return `var(--memory-${palette}-${slot}-color)`;
}

interface LegendRow {
  key: string;
  label: string;
  bytes: number;
  color: string;
  percent: number;
}

function toRows(segments: MemorySegment[], total: number): LegendRow[] {
  return segments.map((segment) => ({
    key: segment.key,
    label: t(SEGMENT_STYLE[segment.key].label),
    bytes: segment.bytes,
    color: segmentColor(segment.key),
    percent: total > 0 ? (segment.bytes / total) * 100 : 0,
  }));
}

function usedFree(used: number, total: number): MemorySegment[] {
  return [
    { key: 'used', bytes: used },
    { key: 'free', bytes: Math.max(0, total - used) },
  ];
}

const blocks = computed(() => {
  const { memory } = props;
  const memorySegments =
    memory.composition ?? usedFree(memory.usedBytes, memory.totalBytes);
  return [
    {
      key: 'memory',
      title: t('memory'),
      usageLabel: t('memoryUsage'),
      usage: memory.usagePercent,
      total: memory.totalBytes,
      rows: toRows(memorySegments, memory.totalBytes),
      extras: [
        {
          key: 'available',
          label: t('memoryAvailable'),
          bytes: memory.availableBytes,
        },
        ...(memory.sharedBytes != null
          ? [
              {
                key: 'shared',
                label: t('memoryShared'),
                bytes: memory.sharedBytes,
              },
            ]
          : []),
      ],
    },
    {
      key: 'swap',
      title: 'Swap',
      usageLabel: t('swapUsage'),
      usage: memory.swap.usagePercent,
      total: memory.swap.totalBytes,
      rows: toRows(
        usedFree(memory.swap.usedBytes, memory.swap.totalBytes),
        memory.swap.totalBytes,
      ),
      extras: [],
    },
  ];
});

function formatShare(percent: number): string {
  if (percent > 0 && percent < 1) return '<1%';
  return `${rounded(percent)}%`;
}
</script>

<template>
  <MetricCard
    class="detail-card"
    icon="fa-solid fa-memory"
    :title="t('memoryAndSwap')"
  >
    <div class="memory-blocks">
      <section v-for="block in blocks" :key="block.key" class="memory-block">
        <div class="memory-block__summary">
          <span>{{ block.usageLabel }}</span>
          <q-badge
            class="memory-block__usage"
            :color="usageColor(block.usage, freeThreshold, midThreshold)"
            text-color="white"
          >
            {{ rounded(block.usage) }}%
          </q-badge>
        </div>

        <div class="memory-block__chart">
          <SegmentedRing
            :segments="
              block.rows.map((row) => ({
                key: row.key,
                value: row.bytes,
                color: row.color,
                title: `${row.label}: ${formatBytes(row.bytes, unit)}`,
              }))
            "
          >
            <span class="memory-block__center-label">{{ block.title }}</span>
            <strong class="memory-block__center-value">{{
              formatBytes(block.total, unit)
            }}</strong>
          </SegmentedRing>
        </div>

        <div class="metric-facts">
          <div v-for="row in block.rows" :key="row.key" class="fact-row">
            <span class="memory-legend__label">
              <i
                class="memory-legend__swatch"
                :style="{ background: row.color }"
              />
              {{ row.label }}
            </span>
            <strong>
              {{ formatBytes(row.bytes, unit) }}
              <small class="memory-legend__share">{{
                formatShare(row.percent)
              }}</small>
            </strong>
          </div>
          <template v-if="block.extras.length > 0">
            <div class="memory-legend__divider" />
            <div
              v-for="extra in block.extras"
              :key="extra.key"
              class="fact-row"
            >
              <span>{{ extra.label }}</span>
              <strong>{{ formatBytes(extra.bytes, unit) }}</strong>
            </div>
          </template>
        </div>
      </section>
    </div>
  </MetricCard>
</template>

<style scoped lang="scss">
.memory-blocks {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(12.5rem, 1fr));
  gap: 0.75rem;
  align-items: start;
}

.memory-block {
  display: grid;
  gap: 0.65rem;
  min-width: 0;
}

.memory-block__summary {
  display: grid;
  gap: 0.15rem;
  padding: 0.65rem 0.8rem;
  border-radius: 12px;
  background: var(--bg-section-color);

  span {
    color: var(--text-muted-color);
    font-size: 0.72rem;
  }
}

.memory-block__usage {
  justify-self: start;
  padding: 0.25rem 0.55rem;
  border-radius: 6px;
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.2;
}

.memory-block__chart {
  display: flex;
  justify-content: center;
}

.memory-block__center-label {
  color: var(--text-muted-color);
  font-size: 0.68rem;
  line-height: 1.2;
}

.memory-block__center-value {
  font-size: 0.82rem;
  line-height: 1.25;
  white-space: nowrap;
}

.memory-legend__label {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  min-width: 0;
}

.memory-legend__swatch {
  flex: none;
  width: 0.65rem;
  height: 0.65rem;
  border-radius: 3px;
  /* Keeps the free (track-colored) swatch visible on the section background. */
  box-shadow: inset 0 0 0 1px var(--border-color);
}

.memory-legend__share {
  display: inline-block;
  min-width: 2.4em;
  margin-left: 0.3rem;
  color: var(--text-muted-color);
  font-weight: 400;
  text-align: right;
}

.memory-legend__divider {
  height: 1px;
  background: var(--divider-color);
}

@media (max-width: 420px) {
  .memory-block__summary span {
    font-size: 0.66rem;
  }

  .memory-block__usage {
    font-size: 0.9rem;
  }
}
</style>
