<script setup lang="ts">
import { computed, type CSSProperties } from 'vue';

import {
  formatCpuFrequency,
  rounded,
  usageColor,
} from '@/shared/format/metrics';

const props = defineProps<{
  index: number;
  usage: number;
  frequencyMhz: number | null | undefined;
  freeThreshold: number;
  midThreshold: number;
}>();

const normalizedUsage = computed(() => Math.min(100, Math.max(0, props.usage)));
const frequencyLabel = computed(() => formatCpuFrequency(props.frequencyMhz));
const tileStyle = computed(
  () =>
    ({
      '--cpu-usage': normalizedUsage.value / 100,
      '--cpu-accent': `var(--${usageColor(
        normalizedUsage.value,
        props.freeThreshold,
        props.midThreshold,
      )})`,
    }) as CSSProperties,
);
</script>

<template>
  <div class="cpu-usage-tile" :style="tileStyle">
    <div class="cpu-usage-tile__fill" aria-hidden="true" />
    <span class="cpu-usage-tile__index">#{{ index + 1 }}</span>
    <div class="cpu-usage-tile__readout">
      <strong>{{ rounded(normalizedUsage) }}%</strong>
      <span>{{ frequencyLabel }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.cpu-usage-tile {
  --cpu-usage: 0;
  --cpu-accent: var(--free-color);

  position: relative;
  isolation: isolate;
  display: grid;
  grid-template-rows: auto 1fr;
  min-width: 0;
  aspect-ratio: 1;
  padding: 0.4rem;
  overflow: hidden;
  border: 1px solid var(--border-color);
  border-radius: 11px;
  background: var(--bg-section-color);
}

.cpu-usage-tile__fill {
  position: absolute;
  inset: 0;
  z-index: -1;
  background: var(--cpu-accent);
  transform: scaleY(var(--cpu-usage));
  transform-origin: bottom;
}

.cpu-usage-tile__index {
  justify-self: start;
  padding: 0.1rem 0.2rem;
  border-radius: 3px;
  background: var(--bg-section-color);
  color: var(--text-card-color);
  font-size: 0.66rem;
  font-weight: 600;
  line-height: 1;
}

.cpu-usage-tile__readout {
  align-self: center;
  justify-self: stretch;
  display: grid;
  gap: 0.05rem;
  padding: 0.26rem 0.18rem;
  border-radius: 7px;
  background: var(--bg-card-color);
  text-align: center;
  line-height: 1.15;

  strong {
    font-size: clamp(0.85rem, 1.1vw, 1.05rem);
  }

  span {
    color: var(--text-muted-color);
    font-size: clamp(0.58rem, 0.75vw, 0.7rem);
    white-space: nowrap;
  }
}
</style>
