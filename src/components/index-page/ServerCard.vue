<template>
  <div class="server-card-wrapper q-pa-sm bg-transparent">
    <div
      class="server-card full-height column justify-center items-center no-wrap bg-card-color rounded-borders q-px-md q-pt-lg"
    >
      <div class="row justify-center items-center full-width">
        <q-icon
          class="cursor-pointer"
          name="dns"
          :style="{ color: server.tagColor }"
          size="md"
        >
          <q-tooltip>
            {{ server.serverUrl }}
          </q-tooltip>
        </q-icon>
        <div class="col-grow row justify-center items-center">
          <span class="text-h6 text-card-color">{{ server.customName }}</span>
        </div>
        <div class="row justify-center items-center">
          <q-icon
            v-if="loadingError.hasError()"
            class="q-mr-xs"
            name="error"
            color="negative"
            size="md"
          >
            <q-tooltip>
              {{ t('loadingFailedTooltip') }}
            </q-tooltip>
          </q-icon>
          <q-btn
            icon="more_vert"
            size="md"
            :to="`/server/${server.uniqueId}`"
            flat
            round
          />
        </div>
      </div>
      <div
        class="col-grow column justify-start items-center full-width full-height no-wrap q-pt-md"
      >
        <div class="row justify-between items-start no-wrap full-width">
          <CircularProgressWithTitle
            :title="t('cpuUsage')"
            :color="
              getUsageColorClass(
                cpuState?.cpuUsage.avg,
                props.freeUsageThreshold,
                props.midUsageThreshold
              )
            "
            :value="rounded(cpuState?.cpuUsage.avg, 0)"
            :show-value-text="`${rounded(cpuState?.cpuUsage.avg, 0)}%`"
            :is-error="loadingError.cpuStateFetchError"
            :size="cpuProgressSize"
            :inner-text-size-percentage="innerTextSizePercentage"
          />
          <CircularProgressWithTitle
            :title="t('memoryUsage')"
            :color="
              getUsageColorClass(
                memoryState?.memoryPercent,
                props.freeUsageThreshold,
                props.midUsageThreshold
              )
            "
            :value="rounded(memoryState?.memoryPercent, 0)"
            :show-value-text="`${rounded(memoryState?.memoryPercent, 0)}%`"
            :is-error="loadingError.memoryStateFetchError"
            :size="cpuProgressSize"
            :inner-text-size-percentage="innerTextSizePercentage"
          />
          <CircularProgressWithTitle
            :title="t('swapUsage')"
            :color="
              getUsageColorClass(
                memoryState?.swapPercent,
                props.freeUsageThreshold,
                props.midUsageThreshold
              )
            "
            :value="rounded(memoryState?.swapPercent, 0)"
            :show-value-text="`${rounded(memoryState?.swapPercent, 0)}%`"
            :is-error="loadingError.memoryStateFetchError"
            :size="cpuProgressSize"
            :inner-text-size-percentage="innerTextSizePercentage"
          />
        </div>
        <CpuInfoRow
          class="q-mt-md"
          v-if="props.showLayout !== 'sm' && cpuState && cpuName"
          :cpu-name="cpuName"
          :cpu-state="cpuState"
          :show-layout="showLayout"
          :free-usage-threshold="props.freeUsageThreshold"
          :mid-usage-threshold="props.midUsageThreshold"
          :use-fahrenheit-unit="props.useFahrenheitUnit"
        />
        <div
          v-if="server.gpuServer.gpuType !== GPUType.NoneGPU && gpuState"
          class="row justify-center items-center no-wrap full-width q-mt-md"
        >
          <GpuInfoRow
            :gpu-state="gpuState"
            :show-layout="props.showLayout"
            :free-usage-threshold="props.freeUsageThreshold"
            :mid-usage-threshold="props.midUsageThreshold"
            :size="gpuProgressSize"
            :inner-text-size-percentage="innerTextSizePercentage"
            :is-error="loadingError.gpuStateFetchError"
            :gpu-memory-unit="props.gpuMemoryUnit"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ByteUnit, GPUType, ServerConfig } from 'src/module/config';
import {
  inject,
  onBeforeUnmount,
  onMounted,
  PropType,
  reactive,
  ref,
  watch,
} from 'vue';
import {
  CPUNameResponse,
  CPUStatePerCPUResponse,
  GPUStateResponse,
  MemoryStateResponse,
} from 'src/interface/api';
import API from 'src/api/api';
import { useI18n } from 'vue-i18n';
import { useInterval } from 'quasar';
import { getUsageColorClass, rounded } from 'src/utils/utils';
import CircularProgressWithTitle from 'components/base/CircularProgressWithTitle.vue';
import { LoadingError } from 'src/module/loading-error';
import GpuInfoRow from 'components/base/GPUInfoRow.vue';
import CpuInfoRow from 'components/base/CPUInfoRow.vue';

const props = defineProps({
  serverConfig: {
    type: Object as PropType<ServerConfig>,
    required: true,
  },
  showLayout: {
    type: String,
    default: 'sm',
    validator(val: string) {
      return ['sm', 'md', 'lg'].includes(val);
    },
  },
  useFahrenheitUnit: {
    type: Boolean,
    default: false,
  },
  refreshTimeSec: {
    type: Number,
    default: 1,
    validator(val: number) {
      return val >= 1;
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
  memoryUnit: {
    type: String,
    default: ByteUnit.GB,
    validator(val: ByteUnit) {
      return [ByteUnit.GB, ByteUnit.TB].includes(val);
    },
  },
  gpuMemoryUnit: {
    type: String,
    default: ByteUnit.GB,
    validator(val: ByteUnit) {
      return [ByteUnit.GB, ByteUnit.TB].includes(val);
    },
  },
});

const { t } = useI18n();
const {
  registerInterval: cpuStateRegisterInterval,
  removeInterval: cpuStateRemoveInterval,
} = useInterval();

const {
  registerInterval: memoryStateRegisterInterval,
  removeInterval: memoryStateRemoveInterval,
} = useInterval();

const {
  registerInterval: gpuStateRegisterInterval,
  removeInterval: gpuStateRemoveInterval,
} = useInterval();

const server = ref(props.serverConfig);
const cpuState = ref<CPUStatePerCPUResponse>();
const cpuName = ref<CPUNameResponse>();
const memoryState = ref<MemoryStateResponse>();
const gpuState = ref<GPUStateResponse>();
const loadingError = reactive(new LoadingError());
const pauseFetchInject = inject('pauseFetch', false);
const pauseFetch = ref<boolean>(pauseFetchInject);
const cpuProgressSize = ref(4);
const gpuProgressSize = ref(3);
const innerTextSizePercentage = ref(0.2);

function getCpuName() {
  if (!pauseFetch.value) {
    API.getCpuName<CPUNameResponse>(server.value.serverUrl)
      .then((res) => {
        cpuName.value = res;
        loadingError.cpuNameFetchError = false;
      })
      .catch(() => {
        loadingError.cpuNameFetchError = true;
      });
  }
}

function getCpuState() {
  if (!pauseFetch.value) {
    API.getCpuState<CPUStatePerCPUResponse>(
      server.value.serverUrl,
      true,
      props.useFahrenheitUnit
    )
      .then((res) => {
        cpuState.value = res;
        loadingError.cpuStateFetchError = false;
      })
      .catch(() => {
        loadingError.cpuStateFetchError = true;
      });
  }
}

function getMemoryState() {
  if (!pauseFetch.value) {
    API.getMemoryState<MemoryStateResponse>(
      server.value.serverUrl,
      props.memoryUnit
    )
      .then((res) => {
        memoryState.value = res;
        loadingError.memoryStateFetchError = false;
      })
      .catch(() => {
        loadingError.memoryStateFetchError = true;
      });
  }
}

function getNVGPUState() {
  if (!pauseFetch.value) {
    API.getNVGPUState<GPUStateResponse>(
      server.value.serverUrl,
      props.gpuMemoryUnit,
      props.useFahrenheitUnit
    )
      .then((res) => {
        gpuState.value = res;
        loadingError.gpuStateFetchError = false;
      })
      .catch(() => {
        loadingError.gpuStateFetchError = true;
      });
  }
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
  getCpuName();
  cpuStateRegisterInterval(() => {
    getCpuName();
    getCpuState();
  }, props.refreshTimeSec * 1000);
  memoryStateRegisterInterval(
    () => getMemoryState(),
    props.refreshTimeSec * 1000
  );
  gpuStateRegisterInterval(() => getGPUState(), props.refreshTimeSec * 1000);
});

watch(
  props,
  () => {
    cpuStateRemoveInterval();
    memoryStateRemoveInterval();
    gpuStateRemoveInterval();
    cpuStateRegisterInterval(() => {
      getCpuName();
      getCpuState();
    }, props.refreshTimeSec * 1000);
    memoryStateRegisterInterval(
      () => getMemoryState(),
      props.refreshTimeSec * 1000
    );
    gpuStateRegisterInterval(() => getGPUState(), props.refreshTimeSec * 1000);
  },
  {
    deep: true,
  }
);

onBeforeUnmount(() => {
  cpuStateRemoveInterval();
  memoryStateRemoveInterval();
  gpuStateRemoveInterval();
});
</script>

<style lang="sass" scoped>
.server-card-wrapper
  .server-card
    transition: all 0.2s ease-in-out
</style>
