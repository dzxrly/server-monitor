<script setup lang="ts">
import { computed, inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';

import CpuPanel from '@/features/monitoring/components/detail/CpuPanel.vue';
import GpuPanel from '@/features/monitoring/components/detail/GpuPanel.vue';
import MemoryPanel from '@/features/monitoring/components/detail/MemoryPanel.vue';
import NetworkPanel from '@/features/monitoring/components/detail/NetworkPanel.vue';
import StoragePanel from '@/features/monitoring/components/detail/StoragePanel.vue';
import SystemPanel from '@/features/monitoring/components/detail/SystemPanel.vue';
import TemperaturePanel from '@/features/monitoring/components/detail/TemperaturePanel.vue';
import { POLLING_PAUSED_KEY } from '@/features/monitoring/composables/polling-context';
import { useServerMetrics } from '@/features/monitoring/composables/use-server-metrics';
import { useConfigStore } from '@/features/settings/stores/config-store';

const route = useRoute();
const { t } = useI18n();
const configStore = useConfigStore();
const paused = inject(POLLING_PAUSED_KEY, ref(false));
const server = computed(() =>
  configStore.config.serverListConfig.find(
    (item) => item.uniqueId === route.params.uid,
  ),
);
const serverUrl = computed(
  () => server.value?.serverUrl ?? 'http://127.0.0.1:0',
);
const refreshSeconds = computed(() => configStore.config.refreshTimeSec);
const processLimit = computed(() => configStore.config.processLimit);
const { metrics, error, loading, refreshing, refresh } = useServerMetrics({
  serverUrl,
  refreshSeconds,
  processLimit,
  paused,
});
</script>

<template>
  <q-page class="detail-page q-px-sm q-pb-md q-px-md-md">
    <div v-if="!server" class="empty-page column items-center justify-center">
      <q-icon name="delete_forever" size="xl" />
      <div class="text-h6 q-mt-sm">{{ t('serverNotFound') }}</div>
      <q-btn
        flat
        rounded
        no-caps
        icon="arrow_back"
        to="/"
        :label="t('back')"
        class="q-mt-md"
      />
    </div>
    <template v-else>
      <header
        class="detail-header bg-default-color row items-center no-wrap q-py-sm"
      >
        <q-btn flat round icon="arrow_back" to="/" />
        <q-icon
          name="dns"
          size="sm"
          class="q-ml-xs"
          :style="{ color: server.tagColor }"
        />
        <div class="col q-ml-sm min-width-zero">
          <div class="text-h6 ellipsis">{{ server.customName }}</div>
          <div class="text-caption text-muted-color ellipsis">
            {{ server.serverUrl }}
          </div>
        </div>
        <q-btn
          flat
          round
          icon="refresh"
          :loading="refreshing"
          :disable="paused"
          :aria-label="t('refresh')"
          @click="refresh"
        />
      </header>

      <q-banner v-if="error" rounded class="bg-negative text-white q-mb-md">
        <template #avatar><q-icon name="error" /></template>
        {{ t('loadingFailedTooltip') }} · {{ error }}
      </q-banner>
      <div v-if="loading && !metrics" class="column items-center q-pa-xl">
        <q-spinner color="primary" size="3rem" />
      </div>
      <div v-else-if="metrics" class="detail-grid">
        <CpuPanel
          :cpu="metrics.cpu"
          :processes="metrics.processes.cpu"
          :fahrenheit="configStore.config.useFahrenheitUnit"
          :free-threshold="configStore.config.freeUsageThreshold"
          :mid-threshold="configStore.config.midUsageThreshold"
        />
        <MemoryPanel
          :memory="metrics.memory"
          :processes="metrics.processes.memory"
          :unit="configStore.config.memoryUnit"
          :free-threshold="configStore.config.freeUsageThreshold"
          :mid-threshold="configStore.config.midUsageThreshold"
        />
        <GpuPanel
          :gpu="metrics.gpu"
          :processes="metrics.processes.gpu"
          :unit="configStore.config.gpuMemoryUnit"
          :fahrenheit="configStore.config.useFahrenheitUnit"
          :free-threshold="configStore.config.freeUsageThreshold"
          :mid-threshold="configStore.config.midUsageThreshold"
        />
        <StoragePanel
          :storage="metrics.storage"
          :unit="configStore.config.memoryUnit"
          :free-threshold="configStore.config.freeUsageThreshold"
          :mid-threshold="configStore.config.midUsageThreshold"
        />
        <NetworkPanel :network="metrics.network" />
        <TemperaturePanel
          :temperatures="metrics.temperatures"
          :fahrenheit="configStore.config.useFahrenheitUnit"
        />
        <SystemPanel :system="metrics.system" />
      </div>
    </template>
  </q-page>
</template>

<style scoped lang="scss">
.detail-page {
  max-width: 1500px;
  margin: 0 auto;
}

.detail-header {
  position: sticky;
  top: 0;
  z-index: 5;
  min-height: 4rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 0.85rem;

  :deep(.detail-card) {
    grid-column: span 4;
  }

  :deep(.detail-card-wide) {
    grid-column: span 8;
  }
}

.empty-page {
  min-height: 70vh;
}

.min-width-zero {
  min-width: 0;
}

@media (max-width: 1100px) {
  .detail-grid {
    :deep(.detail-card),
    :deep(.detail-card-wide) {
      grid-column: span 6;
    }
  }
}

@media (max-width: 700px) {
  .detail-grid {
    grid-template-columns: 1fr;

    :deep(.detail-card),
    :deep(.detail-card-wide) {
      grid-column: 1;
    }
  }
}
</style>
