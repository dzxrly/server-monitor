<script setup lang="ts">
import { computed } from 'vue';

export interface RingSegment {
  key: string;
  value: number;
  color: string;
  title?: string;
}

const props = withDefaults(
  defineProps<{
    segments: RingSegment[];
    size?: string;
    thickness?: number;
  }>(),
  {
    size: '5.5rem',
    thickness: 0.16,
  },
);

// Geometry in a 100x100 viewBox; the gap shows the card surface between segments.
const strokeWidth = computed(() => 50 * props.thickness);
const radius = computed(() => 50 - strokeWidth.value / 2);
const circumference = computed(() => 2 * Math.PI * radius.value);
const GAP = 2;
const MIN_ARC = 0.8;

const arcs = computed(() => {
  const visible = props.segments.filter((segment) => segment.value > 0);
  const total = visible.reduce((sum, segment) => sum + segment.value, 0);
  if (total <= 0) return [];
  const gap = visible.length > 1 ? GAP : 0;
  let start = 0;
  return visible.map((segment) => {
    const length = (circumference.value * segment.value) / total;
    const arc = {
      ...segment,
      dasharray: `${Math.max(length - gap, MIN_ARC)} ${circumference.value}`,
      dashoffset: -start,
    };
    start += length;
    return arc;
  });
});
</script>

<template>
  <div class="segmented-ring" :style="{ width: size, height: size }">
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <circle
        v-if="arcs.length === 0"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        stroke="var(--progress-track-color)"
        :stroke-width="strokeWidth"
      />
      <circle
        v-for="arc in arcs"
        :key="arc.key"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke="arc.color"
        :stroke-width="strokeWidth"
        :stroke-dasharray="arc.dasharray"
        :stroke-dashoffset="arc.dashoffset"
        transform="rotate(-90 50 50)"
        class="segmented-ring__arc"
      >
        <title v-if="arc.title">{{ arc.title }}</title>
      </circle>
    </svg>
    <div class="segmented-ring__center">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.segmented-ring {
  position: relative;
  flex: none;
}

.segmented-ring svg {
  display: block;
  width: 100%;
  height: 100%;
}

.segmented-ring__arc {
  transition:
    stroke-dasharray 0.4s ease,
    stroke-dashoffset 0.4s ease;
}

.segmented-ring__center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  pointer-events: none;
}
</style>
