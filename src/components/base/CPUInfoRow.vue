<template>
  <div
    class="cpu-info-row-wrapper column justify-center items-center no-wrap full-width"
  >
    <div class="row justify-start items-center full-width no-wrap">
      <q-icon class="q-mr-xs" name="mdi-cpu-64-bit" size="xs" />
      <span class="text-card-color text-subtitle2 q-mr-xs">
        {{
          props.cpuName.cpuName.split('@')[0].trim().split('CPU')[0].trim()
        }}</span
      >
      <q-badge
        v-if="cpuState.cpuTemperature && cpuState.cpuTemperature.length >= 2"
        class="text-card-color text-subtitle2 cursor-pointer"
        rounded
        color="default-color"
      >
        ×{{ cpuState.cpuTemperature.length }}
        <q-tooltip>
          {{ t('NumaNode') }}
        </q-tooltip>
      </q-badge>
    </div>
    <div class="row justify-between items-center full-width no-wrap q-mt-sm">
      <div class="row justify-center items-center no-wrap">
        <q-icon name="mdi-apps" size="xs" />
        <span class="text-card-color text-body2">
          {{ `${cpuState.cpuCores.cores}C${cpuState.cpuCores.threads}T` }}</span
        >
      </div>
      <div class="row justify-center items-center no-wrap">
        <q-icon name="mdi-approximately-equal" size="xs" />
        <span class="text-card-color text-body2">
          {{ `${rounded(cpuState.cpuFreq.avg.current, 2)}MHz` }}</span
        >
      </div>
      <div class="row justify-center items-center no-wrap">
        <q-icon name="mdi-thermometer" size="xs" />
        <span class="text-card-color text-body2">
          {{
            `${rounded(avgTemp, 2)}${getDegreeUnit(props.useFahrenheitUnit)}`
          }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CPUNameResponse, CPUStatePerCPUResponse } from 'src/interface/api';
import { computed, PropType } from 'vue';
import { getDegreeUnit, rounded } from 'src/utils/utils';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  cpuName: {
    type: Object as PropType<CPUNameResponse>,
    required: true,
  },
  cpuState: {
    type: Object as PropType<CPUStatePerCPUResponse>,
    required: true,
  },
  showLayout: {
    type: String,
    default: 'sm',
    validator(val: string) {
      return ['sm', 'md', 'lg'].includes(val);
    },
  },
  freeUsageThreshold: {
    type: Number,
    default: 20,
    validator(val: number) {
      return val >= 0 && val <= 100;
    },
  },
  midUsageThreshold: {
    type: Number,
    default: 60,
    validator(val: number) {
      return val >= 0 && val <= 100;
    },
  },
  useFahrenheitUnit: {
    type: Boolean,
    default: false,
  },
});

const { t } = useI18n();

const avgTemp = computed(() => {
  return (
    props.cpuState.cpuTemperature.reduce(
      (acc, cur) => acc + (cur.numaCurrent ? cur.numaCurrent : 0),
      0
    ) / props.cpuState.cpuTemperature.length
  );
});
</script>
