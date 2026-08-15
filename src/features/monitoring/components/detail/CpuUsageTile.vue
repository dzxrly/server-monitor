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
      '--cpu-usage': `${normalizedUsage.value}%`,
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
    <div class="cpu-usage-tile__grid" aria-hidden="true" />
    <span class="cpu-usage-tile__index">#{{ index + 1 }}</span>
    <div class="cpu-usage-tile__readout">
      <strong>{{ rounded(normalizedUsage) }}%</strong>
      <span>{{ frequencyLabel }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.cpu-usage-tile {
  --cpu-usage: 0%;
  --cpu-accent: var(--free-color);

  position: relative;
  isolation: isolate;
  display: grid;
  grid-template-rows: auto 1fr;
  min-width: 0;
  aspect-ratio: 1;
  padding: 0.4rem;
  overflow: hidden;
  border: 1px solid
    color-mix(in srgb, var(--cpu-accent) 55%, var(--border-color));
  border-radius: 11px;
  background: color-mix(in srgb, var(--bg-default-color) 78%, transparent);
}

.cpu-usage-tile__fill {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: -2;
  height: var(--cpu-usage);
  background: var(--cpu-accent);
  opacity: 0.72;
  transition:
    height 0.25s ease,
    background-color 0.25s ease;
}

.cpu-usage-tile__grid {
  position: absolute;
  inset: 0;
  z-index: -1;
  background-image:
    linear-gradient(to right, var(--border-color) 1px, transparent 1px),
    linear-gradient(to bottom, var(--border-color) 1px, transparent 1px);
  background-size: 25% 25%;
  opacity: 0.65;
}

.cpu-usage-tile__index {
  color: var(--text-muted-color);
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
  background: color-mix(in srgb, var(--bg-card-color) 86%, transparent);
  text-align: center;
  line-height: 1.15;
  backdrop-filter: blur(2px);

  strong {
    font-size: clamp(0.85rem, 1.1vw, 1.05rem);
  }

  span {
    color: var(--text-muted-color);
    font-size: clamp(0.58rem, 0.75vw, 0.7rem);
    white-space: nowrap;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cpu-usage-tile__fill {
    transition: none;
  }
}
</style>
