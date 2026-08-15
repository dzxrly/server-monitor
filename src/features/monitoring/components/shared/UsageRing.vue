<script setup lang="ts">
import { computed } from 'vue';

import { rounded, usageColor } from '@/shared/format/metrics';

const props = withDefaults(
  defineProps<{
    label: string;
    value: number | null | undefined;
    freeThreshold?: number;
    midThreshold?: number;
    size?: string;
    thickness?: number;
  }>(),
  {
    freeThreshold: 30,
    midThreshold: 70,
    size: '4.25rem',
    thickness: 0.16,
  },
);

const normalizedValue = computed(() =>
  Math.min(100, Math.max(0, props.value ?? 0)),
);
const color = computed(() =>
  usageColor(normalizedValue.value, props.freeThreshold, props.midThreshold),
);
</script>

<template>
  <div class="column items-center no-wrap usage-ring">
    <q-circular-progress
      show-value
      :value="normalizedValue"
      :color="color"
      track-color="progress-track"
      :size="size"
      :thickness="thickness"
      class="text-weight-medium"
    >
      {{ rounded(normalizedValue) }}%
    </q-circular-progress>
    <span class="text-caption text-card-color q-mt-xs text-center">{{
      label
    }}</span>
  </div>
</template>

<style scoped>
.usage-ring {
  min-width: 4.5rem;
}
</style>
