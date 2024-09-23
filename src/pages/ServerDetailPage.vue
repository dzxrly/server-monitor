<script setup lang="ts">
import { useConfigStore } from 'stores/user-config';
import { inject, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { GPUType, ServerConfig } from 'src/module/config';
import { useInterval, useQuasar } from 'quasar';
import { useI18n } from 'vue-i18n';
import {
  CPUNameResponse,
  CPUStatePerCPUResponse,
  GPUStateResponse,
  MemoryStateResponse,
  OSInfoResponse,
} from 'src/interface/api';
import { LoadingError } from 'src/module/loading-error';
import API from 'src/api/api';
import CPUInfoCard from 'components/server-detail-page/CPUInfoCard.vue';
import GPUInfoCard from 'components/server-detail-page/GPUInfoCard.vue';
import MemoryInfoCard from 'components/server-detail-page/MemoryInfoCard.vue';
import OSInfoCard from 'components/server-detail-page/OSInfoCard.vue';

const $route = useRoute();
const $router = useRouter();
const configStore = useConfigStore();
const $q = useQuasar();
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

const server = ref<ServerConfig | undefined>(
  configStore.config.serverListConfig.find(
    (server: ServerConfig) => server.uniqueId === ($route.params.uid as string)
  )
);
const cpuState = ref<CPUStatePerCPUResponse>();
const cpuName = ref<CPUNameResponse>();
const memoryState = ref<MemoryStateResponse>();
const gpuState = ref<GPUStateResponse>();
const osInfo = ref<OSInfoResponse>();
const loadingError = reactive(new LoadingError());
const pauseFetchInject = inject('pauseFetch', false);
const pauseFetch = ref<boolean>(pauseFetchInject);
const cpuUsageCubeSize = ref(5);
const cpuUsageInnerTextPercentage = ref(0.15);

const isLtSm = inject('isLtSm', false);

function getCpuName() {
  if (server.value) {
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
  if (!pauseFetch.value && server.value) {
    API.getCpuState<CPUStatePerCPUResponse>(
      server.value.serverUrl,
      true,
      configStore.config.useFahrenheitUnit
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
  if (!pauseFetch.value && server.value) {
    API.getMemoryState<MemoryStateResponse>(
      server.value.serverUrl,
      configStore.config.memoryUnit
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

function getOSInfo() {
  if (server.value) {
    API.getOSInfo<OSInfoResponse>(server.value.serverUrl)
      .then((res) => {
        osInfo.value = res;
        loadingError.osInfoFetchError = false;
      })
      .catch(() => {
        loadingError.osInfoFetchError = true;
      });
  }
}

function getNVGPUState() {
  if (!pauseFetch.value && server.value) {
    API.getNVGPUState<GPUStateResponse>(
      server.value.serverUrl,
      configStore.config.gpuMemoryUnit,
      configStore.config.useFahrenheitUnit
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
  getOSInfo();
  cpuStateRegisterInterval(
    () => getCpuState(),
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

watch(
  () => configStore,
  () => {
    cpuStateRemoveInterval();
    memoryStateRemoveInterval();
    gpuStateRemoveInterval();
    getCpuName();
    getOSInfo();
    cpuStateRegisterInterval(
      () => getCpuState(),
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
  },
  {
    deep: true,
  }
);

watch(
  () => configStore,
  () => {
    if (
      configStore.config.serverListConfig.findIndex(
        (server: ServerConfig) =>
          server.uniqueId === ($route.params.uid as string)
      ) === -1
    ) {
      $q.notify({
        message: `${t('serverRouteFailed')}${$route.params.uid as string}`,
        type: 'negative',
      });
      $router.push('/');
    }
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

<template>
  <q-page
    class="server-detail-page-wrapper column justify-center items-center full-width"
    :class="isLtSm ? 'q-px-sm q-pb-sm' : 'q-px-md q-pb-sm'"
  >
    <div
      v-if="server === undefined"
      class="full-width full-height column justify-center items-center"
    >
      <q-icon name="delete_forever" size="xl" color="primary" />
      <span class="text-default-color text-h6 q-mt-xs">{{
        t('serverNotFound')
      }}</span>
      <span class="text-default-color text-subtitle2 q-mt-xs">{{
        $route.params.uid as string
      }}</span>
    </div>
    <div
      v-else
      class="full-width full-height column justify-start items-center col-grow"
    >
      <div
        class="server-detail-title bg-default-color row justify-start items-center no-wrap full-width q-py-sm"
      >
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
          :style="{ color: server.tagColor }"
        />
        <span class="text-default-color text-h6">{{ server.customName }}</span>
      </div>
      <CPUInfoCard
        v-if="cpuState && cpuName"
        :cpu-state="cpuState"
        :cpu-name="cpuName"
        :cpu-usage-cube-size="cpuUsageCubeSize"
        :cpu-usage-inner-text-percentage="cpuUsageInnerTextPercentage"
      />
      <MemoryInfoCard
        class="q-mt-md"
        v-if="memoryState"
        :memory-state="memoryState"
        :memory-unit="configStore.config.memoryUnit"
      />
      <GPUInfoCard
        class="q-mt-md"
        v-if="gpuState"
        :gpu-state="gpuState"
        :is-error="loadingError.gpuStateFetchError"
        :use-fahrenheit-unit="configStore.config.useFahrenheitUnit"
        :gpu-memory-unit="configStore.config.gpuMemoryUnit"
      />
      <OSInfoCard
        class="q-mt-md"
        v-if="osInfo"
        :os-name="osInfo.osName"
        :os-architecture="osInfo.osArchitecture"
        :os-sign="osInfo.osSign"
        :os-node="osInfo.osNode"
        :os-bits="osInfo.osBits"
        :os-kernel="osInfo.osKernel"
      />
    </div>
  </q-page>
</template>

<style lang="sass" scoped>
.server-detail-page-wrapper
  .server-detail-title
    position: sticky
    top: 0
    z-index: 3
</style>
