<template>
  <div
    class="gpu-info-row-wrapper column justify-center items-center no-wrap full-width"
  >
    <div
      v-if="props.showLayout === 'sm'"
      class="column justify-center items-center no-wrap full-width"
    >
      <div class="row justify-center no-wrap items-center full-width">
        <q-icon
          class="text-card-color q-mr-xs"
          name="mdi-expansion-card"
          size="md"
        />
        <span class="text-card-color text-subtitle2">{{ t('gpuUsage') }}</span>
      </div>
      <div class="gpu-info-row-sm-progress-circle full-width">
        <CircularProgressWithTitle
          v-for="(gpu, index) of props.gpuState?.gpuList"
          :key="index"
          :value="gpu.gpuUsage"
          :show-value-text="`${rounded(gpu.gpuUsage, 0)}%`"
          :color="
            getUsageColorClass(
              gpu.gpuUsage,
              props.freeUsageThreshold,
              props.midUsageThreshold
            )
          "
          :size="props.size"
          :inner-text-size-percentage="props.innerTextSizePercentage"
          :is-error="props.isError"
        />
      </div>
    </div>
    <div v-else class="column justify-center items-center no-wrap full-width">
      <div
        v-for="(gpu, index) of props.gpuState?.gpuList"
        :key="index"
        class="column justify-center items-center no-wrap full-width q-mt-sm"
      >
        <div class="row justify-between items-center no-wrap full-width">
          <div>
            <q-icon
              class="text-card-color q-mr-xs"
              name="mdi-expansion-card"
              size="sm"
            />
            <span
              class="text-card-color text-subtitle2 overflow-hidden ellipsis"
              >{{ gpu.gpuName }}</span
            >
          </div>
          <span class="text-card-color text-subtitle2">{{
            `${rounded(gpu.gpuTemperature, 0)}${getDegreeUnit(
              props.useFahrenheitUnit
            )}`
          }}</span>
        </div>
        <div class="row justify-between items-center no-wrap full-width">
          <span class="col-4 text-card-color text-body2">{{
            t('gpuCoreUsage')
          }}</span>
          <q-linear-progress
            class="col-grow q-ml-xs rounded-borders"
            :value="gpu.gpuUsage / 100"
            :class="
              getUsageColorClass(
                gpu.gpuUsage,
                props.freeUsageThreshold,
                props.midUsageThreshold
              )
            "
            track-color="grey-6"
            size="1.2rem"
          >
            <div class="absolute-full flex flex-center">
              <q-badge
                color="default-color"
                class="text-card-color"
                :label="`${rounded(gpu.gpuUsage, 0)}%`"
              />
            </div>
          </q-linear-progress>
        </div>
        <div
          class="row justify-between items-center no-wrap full-width q-mt-xs"
        >
          <span class="col-4 text-card-color text-body2">{{
            t('gpuMemoryUsage')
          }}</span>
          <q-linear-progress
            class="col-grow q-ml-xs rounded-borders"
            :value="gpu.memoryPercent / 100"
            :class="
              getUsageColorClass(
                gpu.memoryPercent,
                props.freeUsageThreshold,
                props.midUsageThreshold
              )
            "
            track-color="grey-6"
            size="1.2rem"
          >
            <div class="absolute-full flex flex-center">
              <q-badge
                color="default-color"
                class="text-card-color"
                :label="`${rounded(gpu.memoryUsed, gpuMemoryDigit)}/${rounded(
                  gpu.memoryTotal,
                  gpuMemoryDigit
                )} ${props.gpuMemoryUnit}`"
              />
            </div>
          </q-linear-progress>
        </div>
        <div
          v-if="props.showLayout === 'lg'"
          class="row justify-between items-center full-width no-wrap q-mt-xs"
        >
          <q-chip color="default-color" size="sm">
            <q-icon
              class="text-card-color q-mr-xs"
              name="mdi-flash"
              size="0.8rem"
            />
            {{
              `${t('power')} ${rounded(gpu.powerCurrent, 0)}/${rounded(
                gpu.powerLimit,
                0
              )}W`
            }}
          </q-chip>
          <q-chip color="default-color" size="sm">
            <FanIcon
              class="q-mr-xs"
              :fan-speed="gpu.fanSpeed"
              size="0.8rem"
            ></FanIcon>
            {{ `${t('fanSpeed')} ${gpu.fanSpeed}%` }}
          </q-chip>
        </div>
      </div>
      <div
        v-if="props.showLayout === 'lg'"
        class="row justify-end items-center no-wrap full-width q-mt-xs"
      >
        <span class="text-card-color text-caption"
          >{{ t('gpuDriverVersion') }} {{ gpuState.driverVersion }}</span
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, PropType } from 'vue';
import { GPUStateResponse } from 'src/interface/api';
import { useI18n } from 'vue-i18n';
import { getDegreeUnit, getUsageColorClass, rounded } from 'src/utils/utils';
import FanIcon from 'components/base/FanIcon.vue';
import CircularProgressWithTitle from 'components/base/CircularProgressWithTitle.vue';
import { ByteUnit } from 'src/module/config';

const props = defineProps({
  gpuState: {
    type: Object as PropType<GPUStateResponse>,
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
  isError: {
    type: Boolean,
    default: false,
  },
  size: {
    type: Number,
    default: 4,
  },
  innerTextSizePercentage: {
    type: Number,
    default: 0.2,
    validator: (value: number) => {
      return value >= 0 && value <= 1;
    },
  },
  gpuMemoryUnit: {
    type: String,
    default: ByteUnit.GB,
  },
});

const { t } = useI18n();

const progressSize = computed(() => {
  return `${props.size}rem`;
});
const gpuMemoryDigit = computed(() => {
  return props.gpuMemoryUnit === ByteUnit.TB ? 2 : 0;
});
</script>

<style lang="sass" scoped>
.gpu-info-row-wrapper
  .gpu-info-row-sm-progress-circle
    display: grid
    grid-template-columns: repeat(auto-fill, v-bind(progressSize))
    grid-template-rows: repeat(auto-fill, v-bind(progressSize))
    justify-items: center
    align-items: center
    justify-content: center
    align-content: center
    grid-gap: 0.2rem
</style>
