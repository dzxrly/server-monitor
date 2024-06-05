<template>
  <div class="gpu-info-row-wrapper column justify-center items-center no-wrap full-width">
    <div v-if="props.showLayout === 'sm'" class="column justify-center items-center no-wrap full-width">
      <div class="row justify-center no-wrap items-center full-width">
        <q-icon class="text-base-color q-mr-xs" name="mdi-expansion-card" size="md" />
        <span class="text-base-color text-subtitle2">{{ t('gpuUsage') }}</span>
      </div>
      <div class="row justify-start items-center wrap full-width">
        <q-circular-progress
          show-value
          class="q-ma-sm"
          v-for="(gpu, index) of props.gpuState?.gpuList"
          :key="index"
          :value="rounded(gpu.gpuUsage, 0)"
          :class="getUsageColorClass(gpu.gpuUsage, props.freeUsageThreshold, props.midUsageThreshold)"
          :thickness="0.2"
          track-color="grey-4"
          :size="props.gpuState?.gpuList.length <= 4 ? 'xl' : 'md'"
        >
          <span class="text-base-color">{{ rounded(gpu.gpuUsage, 0) }}%</span>
        </q-circular-progress>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from 'vue';
import { GPUStateResponse } from 'src/interface/api';
import { useI18n } from 'vue-i18n';
import { getUsageColorClass, rounded } from 'src/utils/utils';

const props = defineProps({
  gpuState: {
    type: Object as PropType<GPUStateResponse>,
    required: true
  },
  showLayout: {
    type: String,
    default: 'sm',
    validator(val: string) {
      return ['sm', 'md', 'lg'].includes(val);
    }
  },
  freeUsageThreshold: {
    type: Number,
    default: 20,
    validator(val: number) {
      return val >= 0 && val <= 100;
    }
  },
  midUsageThreshold: {
    type: Number,
    default: 60,
    validator(val: number) {
      return val >= 0 && val <= 100;
    }
  }
});

const { t } = useI18n();
</script>
