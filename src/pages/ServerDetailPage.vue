<template>
  <q-page class="server-detail-page-wrapper column justify-center items-center full-width q-pa-md">
    <div
      v-if="server === undefined"
      class="full-width full-height column justify-center items-center">
      <q-icon name="delete_forever" size="xl" color="primary" />
      <span class="text-default-color text-h6 q-mt-xs">{{ t('serverNotFound') }}</span>
      <span class="text-default-color text-subtitle2 q-mt-xs">{{ $route.params.uid as string }}</span>
    </div>
    <div
      v-else
      class="full-width full-height column justify-start items-center col-grow"
    >
      <div class="row justify-start items-center no-wrap full-width">
        <q-btn
          class="q-mr-sm"
          icon="arrow_back"
          color="primary"
          size="md"
          to="/"
          flat
          round
        />
        <q-icon
          class="q-mr-sm"
          name="dns"
          size="md"
          :style="{ color: server.tagColor}"
        />
        <span
          class="text-default-color text-h6"
        >{{ server.customName }}</span>
      </div>
      <div class="row justify-start items-center no-wrap full-width q-px-md q-mt-md">
        <span class="text-card-color text-subtitle2">{{ t('cpuUsage') }}</span>
      </div>
      <div class="bg-card-color full-width column justify-center items-center no-wrap rounded-borders q-pa-md q-mt-sm">
        <div class="row justify-between items-center wrap full-width">
          <div>
            <span
              class="text-card-color text-body2 q-mr-xs">{{ cpuName?.cpuName.split('@')[0].trim().split('CPU')[0].trim()
              }}</span>
            <q-badge
              v-if="cpuState?.cpuTemperature.numaNodeTemperature && cpuState?.cpuTemperature.numaNodeTemperature.length >= 2"
              class="text-card-color text-subtitle2 cursor-pointer"
              rounded
              color="default-color">
              ×{{ cpuState.cpuTemperature.numaNodeTemperature.length }}
              <q-tooltip>
                {{ t('NumaNode') }}
              </q-tooltip>
            </q-badge>
          </div>
          <span class="text-card-color text-body2">{{ `${cpuState?.cpuCores.cores}C${cpuState?.cpuCores.threads}T`
            }}</span>
        </div>
        <div class="row justify-start items-center wrap full-width q-mt-sm">
          <CPUUsageCube
            v-for="(core, index) of cpuState?.cpuUsage.percpu"
            :key="index"
            :cpu-usage="core"
            :cpu-temperature="cpuState && cpuState.cpuTemperature && cpuState.cpuTemperature.coreTemperature && cpuState.cpuTemperature.coreTemperature[index] ? cpuState.cpuTemperature.coreTemperature[index].current : 0"
            :use-fahrenheit="configStore.config.useFahrenheitUnit"
            cube-size="5rem"
            :text-size-percentage="0.5"
            :free-usage-threshold="configStore.config.freeUsageThreshold"
            :mid-usage-threshold="configStore.config.midUsageThreshold"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useConfigStore } from 'stores/user-config';
import { inject, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { GPUType, ServerConfig } from 'src/module/config';
import { useInterval, useQuasar } from 'quasar';
import { useI18n } from 'vue-i18n';
import { CPUNameResponse, CPUStatePerCPUResponse, GPUStateResponse, MemoryStateResponse } from 'src/interface/api';
import { LoadingError } from 'src/module/loading-error';
import API from 'src/api/api';
import CPUUsageCube from 'components/base/CPUUsageCube.vue';

const $route = useRoute();
const $router = useRouter();
const configStore = useConfigStore();
const $q = useQuasar();
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

const server = ref<ServerConfig | undefined>(configStore.config.serverListConfig.find((server: ServerConfig) => server.uniqueId === ($route.params.uid as string)));
const cpuState = ref<CPUStatePerCPUResponse>();
const cpuName = ref<CPUNameResponse>();
const memoryState = ref<MemoryStateResponse>();
const gpuState = ref<GPUStateResponse>();
const loadingError = reactive(new LoadingError());
const pauseFetchInject = inject('pauseFetch', false);
const pauseFetch = ref<boolean>(pauseFetchInject);

function getCpuName() {
  if (!pauseFetch.value && server.value) {
    API.getCpuName(
      server.value.serverUrl
    ).then((res: any) => {
      cpuName.value = res as CPUNameResponse;
      loadingError.cpuNameFetchError = false;
    }).catch(() => {
      loadingError.cpuNameFetchError = true;
    });
  }
}

function getCpuState() {
  if (!pauseFetch.value && server.value) {
    API.getCpuState(
      server.value.serverUrl,
      true,
      configStore.config.useFahrenheitUnit
    ).then((res: any) => {
      cpuState.value = res as CPUStatePerCPUResponse;
      loadingError.cpuStateFetchError = false;
    }).catch(() => {
      loadingError.cpuStateFetchError = true;
    });
  }
}

function getMemoryState() {
  if (!pauseFetch.value && server.value) {
    API.getMemoryState(server.value.serverUrl, 'GB').then((res: any) => {
      memoryState.value = res as MemoryStateResponse;
      loadingError.memoryStateFetchError = false;
    }).catch(() => {
      loadingError.memoryStateFetchError = true;
    });
  }
}

function getNVGPUState() {
  if (!pauseFetch.value && server.value) {
    API.getNVGPUState(
      server.value.serverUrl,
      'GB',
      configStore.config.useFahrenheitUnit
    ).then((res: any) => {
      gpuState.value = res as GPUStateResponse;
      loadingError.gpuStateFetchError = false;
    }).catch(() => {
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
  if (server.value) {
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
}

onMounted(() => {
  getCpuState();
  getMemoryState();
  getGPUState();
  getCpuName();
  cpuStateRegisterInterval(
    () => {
      getCpuName();
      getCpuState();
    },
    configStore.config.refreshTimeSec * 1000
  );
  memoryStateRegisterInterval(
    () => getMemoryState(),
    configStore.config.refreshTimeSec * 1000
  );
  gpuStateRegisterInterval(
    () => getGPUState(),
    configStore.config.refreshTimeSec * 1000
  );
});

watch(() => configStore, () => {
  cpuStateRemoveInterval();
  memoryStateRemoveInterval();
  gpuStateRemoveInterval();
  cpuStateRegisterInterval(
    () => {
      getCpuName();
      getCpuState();
    },
    configStore.config.refreshTimeSec * 1000
  );
  memoryStateRegisterInterval(
    () => getMemoryState(),
    configStore.config.refreshTimeSec * 1000
  );
  gpuStateRegisterInterval(
    () => getGPUState(),
    configStore.config.refreshTimeSec * 1000
  );
}, {
  deep: true
});

onBeforeUnmount(() => {
  cpuStateRemoveInterval();
  memoryStateRemoveInterval();
  gpuStateRemoveInterval();
});

watch(() => configStore, () => {
  if (configStore.config.serverListConfig.findIndex(
    (server: ServerConfig) => server.uniqueId === ($route.params.uid as string)) === -1) {
    $q.notify({
      message: `${t('serverRouteFailed')}${$route.params.uid as string}`,
      type: 'negative'
    });
    $router.push('/');
  }
}, {
  deep: true
});
</script>
