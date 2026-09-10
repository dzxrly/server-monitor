<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import {
  formatBytes,
  formatRate,
  rounded,
  usageColor,
} from '@/shared/format/metrics';

const props = defineProps<{
  storage: MetricsSnapshot['storage'];
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();
const sortedVolumes = computed(() =>
  [...props.storage.volumes].sort(
    (left, right) =>
      right.totalBytes - left.totalBytes ||
      left.mountpoint.localeCompare(right.mountpoint) ||
      left.device.localeCompare(right.device),
  ),
);
</script>

<template>
  <MetricCard
    class="detail-card detail-card-wide"
    icon="storage"
    :title="t('storage')"
  >
    <div v-if="storage.volumes.length > 0" class="volume-grid">
      <section
        v-for="volume in sortedVolumes"
        :key="`${volume.device}-${volume.mountpoint}`"
        class="volume-item"
      >
        <div class="row justify-between items-center no-wrap q-mb-xs">
          <div class="col min-width-zero">
            <div class="text-subtitle2 ellipsis">{{ volume.mountpoint }}</div>
            <div class="text-caption text-muted-color ellipsis">
              {{ volume.device }} · {{ volume.fileSystem || '—' }}
            </div>
          </div>
          <strong class="q-ml-sm">{{ rounded(volume.usagePercent) }}%</strong>
        </div>
        <q-linear-progress
          rounded
          :value="volume.usagePercent / 100"
          :color="usageColor(volume.usagePercent, freeThreshold, midThreshold)"
          track-color="progress-track"
          size="8px"
        />
        <div class="row justify-between text-caption q-mt-xs">
          <span
            >{{ formatBytes(volume.usedBytes, undefined, 'EB') }}
            {{ t('used') }}</span
          >
          <span>{{ formatBytes(volume.totalBytes, undefined, 'EB') }}</span>
        </div>
      </section>
    </div>
    <div v-else class="empty-state text-muted-color">
      {{ t('noStorageData') }}
    </div>

    <div v-if="storage.devices.length > 0" class="q-mt-md">
      <div class="text-caption text-muted-color q-mb-xs">{{ t('diskIo') }}</div>
      <q-markup-table
        flat
        dense
        class="metric-table bg-transparent text-card-color"
      >
        <thead>
          <tr>
            <th class="text-left">{{ t('device') }}</th>
            <th class="text-right">{{ t('read') }}</th>
            <th class="text-right">{{ t('write') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="device in storage.devices" :key="device.name">
            <td class="text-left">{{ device.name }}</td>
            <td class="text-right">
              {{ formatRate(device.readBytesPerSecond) }}
            </td>
            <td class="text-right">
              {{ formatRate(device.writeBytesPerSecond) }}
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </div>
  </MetricCard>
</template>

<style scoped lang="scss">
.volume-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
  gap: 0.65rem;
}

.volume-item {
  padding: 0.7rem;
  border-radius: 12px;
  background: var(--bg-section-color);
}

.min-width-zero {
  min-width: 0;
}
</style>
