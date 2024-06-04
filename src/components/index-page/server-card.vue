<template>
  <div
    class="server-card-wrapper cursor-pointer q-pa-sm bg-transparent">
    <div
      class="server-card full-height column justify-center items-center no-wrap bg-card-color rounded-borders q-px-md q-py-lg">
      <div class="row justify-center items-center full-width">
        <q-icon name="dns" :style="{color: server.tagColor}" size="md" />
        <div class="col-grow row justify-center items-center">
          <span class="text-h6 text-base-color">{{ server.customName }}</span>
        </div>
        <q-icon v-if="loadingError.hasError()" name="error" color="negative" size="md">
          <q-tooltip>
            {{ t('loadingFailedTooltip') }}
          </q-tooltip>
        </q-icon>
      </div>
      <div class="col-grow column justify-start items-center full-width full-height no-wrap q-pt-md">
        <div class="row justify-between items-start no-wrap full-width">
          <CircularProgressWithTitle
            :title="t('cpuUsage')"
            :color="getUsageColorClass(
              cpuState?.cpuUsage.avg,
              props.freeUsageThreshold,
              props.midUsageThreshold
            )"
            :value="rounded(cpuState?.cpuUsage.avg, 0)"
            :is-error="loadingError.cpuStateFetchError"
          />
          <CircularProgressWithTitle
            :title="t('memoryUsage')"
            :color="getUsageColorClass(
              memoryState?.memoryPercent,
              props.freeUsageThreshold,
              props.midUsageThreshold
            )"
            :value="rounded(memoryState?.memoryPercent, 0)"
            :is-error="loadingError.memoryStateFetchError"
          />
          <CircularProgressWithTitle
            :title="t('swapUsage')"
            :color="getUsageColorClass(
              memoryState?.swapPercent,
              props.freeUsageThreshold,
              props.midUsageThreshold
            )"
            :value="rounded(memoryState?.swapPercent, 0)"
            :is-error="loadingError.memoryStateFetchError"
          />
        </div>
        <div v-if="server.gpuServer.gpuType !== GPUType.NoneGPU && gpuState"
             class="row justify-center items-center no-wrap full-width q-mt-md">
          <GpuInfoRow
            :gpu-state="gpuState"
            :show-layout="props.showLayout"
            :free-usage-threshold="props.freeUsageThreshold"
            :mid-usage-threshold="props.midUsageThreshold"></GpuInfoRow>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { GPUType, ServerConfig } from 'src/module/user-config';
import { onBeforeUnmount, onMounted, PropType, reactive, ref } from 'vue';
import { CPUStatePerCPUResponse, GPUStateResponse, MemoryStateResponse } from 'src/interface/api';
import API from 'src/api/api';
import { useI18n } from 'vue-i18n';
import { useInterval } from 'quasar';
import { getUsageColorClass, rounded } from 'src/utils/utils';
import CircularProgressWithTitle from 'components/base/circular-progress-with-title.vue';
import { LoadingError } from 'src/module/loading-error';
import GpuInfoRow from 'components/base/gpu-info-row.vue';

const props = defineProps({
  serverConfig: {
    type: Object as PropType<ServerConfig>,
    required: true
  },
  showLayout: {
    type: String,
    default: 'sm',
    validator(val: string) {
      return ['sm', 'md', 'lg'].includes(val);
    }
  },
  useFahrenheitUnit: {
    type: Boolean,
    default: false
  },
  refreshTimeSec: {
    type: Number,
    default: 1,
    validator(val: number) {
      return val >= 1;
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
const {
  registerInterval: cpuStateRegisterInterval,
  removeInterval: cpuStateRemoveInterval
} = useInterval();

const {
  registerInterval: memoryStateRegisterInterval,
  removeInterval: memoryStateRemoveInterval
} = useInterval();

const {
  registerInterval: gpuStateRegisterInterval,
  removeInterval: gpuStateRemoveInterval
} = useInterval();

const server = ref(props.serverConfig);
const cpuState = ref<CPUStatePerCPUResponse>();
const memoryState = ref<MemoryStateResponse>();
const gpuState = ref<GPUStateResponse>();
const loadingError = reactive(new LoadingError());

function getCpuState() {
  API.getCpuState(
    server.value.serverUrl,
    true,
    props.useFahrenheitUnit
  ).then((res: any) => {
    cpuState.value = res as CPUStatePerCPUResponse;
    loadingError.cpuStateFetchError = false;
  }).catch(() => {
    loadingError.cpuStateFetchError = true;
  });
}

function getMemoryState() {
  API.getMemoryState(server.value.serverUrl, 'GB').then((res: any) => {
    memoryState.value = res as MemoryStateResponse;
    loadingError.memoryStateFetchError = false;
  }).catch(() => {
    loadingError.memoryStateFetchError = true;
  });
}

function getNVGPUState() {
  API.getNVGPUState(server.value.serverUrl, 'GB').then((res: any) => {
    gpuState.value = res as GPUStateResponse;
    loadingError.gpuStateFetchError = false;
  }).catch(() => {
    loadingError.gpuStateFetchError = true;
  });
}

function getAMDGPUState() {
  loadingError.gpuStateFetchError = true;
  // TODO
}

function getIntelGPUState() {
  loadingError.gpuStateFetchError = true;
  // TODO
}

function getGPUState() {
  switch (server.value.gpuServer.gpuType) {
    case GPUType.NVIDIA:
      getNVGPUState();
      break;
    case GPUType.AMD:
      getAMDGPUState();
      break;
    case GPUType.INTEL:
      getIntelGPUState();
      break;
    default:
      break;
  }
}

onMounted(() => {
  getCpuState();
  getMemoryState();
  getGPUState();
  cpuStateRegisterInterval(
    () => getCpuState(),
    props.refreshTimeSec * 1000
  );
  memoryStateRegisterInterval(
    () => getMemoryState(),
    props.refreshTimeSec * 1000
  );
  gpuStateRegisterInterval(
    () => getGPUState(),
    props.refreshTimeSec * 1000
  );
});

onBeforeUnmount(() => {
  cpuStateRemoveInterval();
  memoryStateRemoveInterval();
  gpuStateRemoveInterval();
});
</script>

<style lang="sass" scoped>
.server-card-wrapper
  .server-card
    box-shadow: none
    transition: all 0.2s ease-in-out

  .server-card:hover
    box-shadow: 0 2px 4px -1px #0003, 0 4px 5px #00000024, 0 1px 10px #0000001f
</style>
