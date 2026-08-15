<script setup lang="ts">
import { computed, inject, ref, toRef } from 'vue';
import { useI18n } from 'vue-i18n';

import { POLLING_PAUSED_KEY } from '@/features/monitoring/composables/polling-context';
import { useServerMetrics } from '@/features/monitoring/composables/use-server-metrics';
import UsageRing from '@/features/monitoring/components/shared/UsageRing.vue';
import type {
  PanelLayout,
  ServerConfig,
} from '@/features/settings/model/config';
import {
  formatRate,
  formatTemperature,
  formatUptime,
  rounded,
} from '@/shared/format/metrics';

const props = defineProps<{
  server: ServerConfig;
  layout: PanelLayout;
  refreshSeconds: number;
  processLimit: number;
  fahrenheit: boolean;
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();
const paused = inject(POLLING_PAUSED_KEY, ref(false));
const serverUrl = computed(() => props.server.serverUrl);
const refreshSeconds = toRef(props, 'refreshSeconds');
const processLimit = toRef(props, 'processLimit');
const { metrics, error, loading } = useServerMetrics({
  serverUrl,
  refreshSeconds,
  processLimit,
  paused,
});

const gpuUsage = computed(
  () => metrics.value?.gpu.devices[0]?.usagePercent ?? 0,
);
const hottestTemperature = computed(() => {
  const sensors = metrics.value?.temperatures.sensors ?? [];
  return sensors.length > 0
    ? Math.max(...sensors.map((sensor) => sensor.currentCelsius))
    : null;
});
const fullestVolume = computed(() => {
  const volumes = metrics.value?.storage.volumes ?? [];
  return volumes.length > 0
    ? volumes.reduce((highest, volume) =>
        volume.usagePercent > highest.usagePercent ? volume : highest,
      )
    : undefined;
});
</script>

<template>
  <q-card
    flat
    class="server-card bg-card-color text-card-color rounded-borders"
  >
    <q-card-section class="column no-wrap full-height q-pa-md">
      <header class="row items-center no-wrap">
        <q-icon name="dns" size="sm" :style="{ color: server.tagColor }">
          <q-tooltip>{{ server.serverUrl }}</q-tooltip>
        </q-icon>
        <div class="col q-ml-sm min-width-zero">
          <div class="text-subtitle1 text-weight-medium ellipsis">
            {{ server.customName }}
          </div>
          <div class="text-caption text-muted-color ellipsis">
            {{ metrics?.system.hostname || server.serverUrl }}
          </div>
        </div>
        <q-spinner v-if="loading" size="xs" color="primary" />
        <q-icon v-else-if="error" name="error" color="negative" size="sm">
          <q-tooltip>{{ error }}</q-tooltip>
        </q-icon>
        <span
          v-else
          class="status-dot status-online"
          :aria-label="t('online')"
        />
        <q-btn
          flat
          round
          dense
          icon="more_vert"
          :to="{ name: 'ServerDetail', params: { uid: server.uniqueId } }"
          :aria-label="t('serverDetails')"
        />
      </header>

      <div class="usage-row q-mt-md">
        <UsageRing
          :label="t('cpuUsage')"
          :value="metrics?.cpu.usagePercent"
          :free-threshold="freeThreshold"
          :mid-threshold="midThreshold"
          size="3.85rem"
        />
        <UsageRing
          :label="t('memoryUsage')"
          :value="metrics?.memory.usagePercent"
          :free-threshold="freeThreshold"
          :mid-threshold="midThreshold"
          size="3.85rem"
        />
        <UsageRing
          :label="metrics?.gpu.available ? t('gpuUsage') : t('swapUsage')"
          :value="
            metrics?.gpu.available
              ? gpuUsage
              : metrics?.memory.swap.usagePercent
          "
          :free-threshold="freeThreshold"
          :mid-threshold="midThreshold"
          size="3.85rem"
        />
      </div>

      <div v-if="layout !== 'sm' && metrics" class="compact-facts q-mt-md">
        <div>
          <q-icon name="download" />
          <span>{{
            formatRate(metrics.network.totals.bytesReceivedPerSecond)
          }}</span>
        </div>
        <div>
          <q-icon name="upload" />
          <span>{{
            formatRate(metrics.network.totals.bytesSentPerSecond)
          }}</span>
        </div>
        <div>
          <q-icon name="mdi-thermometer" />
          <span>{{ formatTemperature(hottestTemperature, fahrenheit) }}</span>
        </div>
        <div>
          <q-icon name="storage" />
          <span>{{
            fullestVolume
              ? `${fullestVolume.mountpoint} ${rounded(fullestVolume.usagePercent)}%`
              : '—'
          }}</span>
        </div>
      </div>

      <div v-if="layout === 'lg' && metrics" class="detail-strip q-mt-md">
        <span class="ellipsis">{{ metrics.cpu.name }}</span>
        <span
          >{{ t('uptime') }}
          {{ formatUptime(metrics.system.uptimeSeconds) }}</span
        >
      </div>
    </q-card-section>
  </q-card>
</template>

<style scoped lang="scss">
.server-card {
  min-height: 12rem;
  border: 1px solid var(--border-color);
  box-shadow: var(--card-shadow);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }
}

.min-width-zero {
  min-width: 0;
}

.usage-row {
  display: flex;
  justify-content: space-around;
  gap: 0.25rem;
}

.status-dot {
  width: 0.55rem;
  height: 0.55rem;
  margin: 0 0.35rem;
  border-radius: 50%;
}

.status-online {
  background: var(--free-color);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--free-color), transparent 78%);
}

.compact-facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.35rem 0.6rem;
  font-size: 0.78rem;

  > div {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    min-width: 0;
  }
}

.detail-strip {
  display: grid;
  gap: 0.2rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border-color);
  color: var(--text-muted-color);
  font-size: 0.74rem;
}
</style>
