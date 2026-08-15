<script setup lang="ts">
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import ProcessTable from '@/features/monitoring/components/shared/ProcessTable.vue';
import UsageRing from '@/features/monitoring/components/shared/UsageRing.vue';
import type { ByteUnit } from '@/features/settings/model/config';
import {
  formatBytes,
  formatTemperature,
  rounded,
} from '@/shared/format/metrics';

defineProps<{
  gpu: MetricsSnapshot['gpu'];
  processes: MetricsSnapshot['processes']['gpu'];
  unit: ByteUnit;
  fahrenheit: boolean;
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();
</script>

<template>
  <MetricCard
    class="detail-card"
    icon="mdi-expansion-card"
    :title="t('gpuInfo')"
  >
    <template v-if="gpu.devices.length > 0">
      <section
        v-for="device in gpu.devices"
        :key="device.uuid || device.index"
        class="gpu-device"
      >
        <div class="text-subtitle2 ellipsis q-mb-sm">{{ device.name }}</div>
        <div class="row justify-around q-gutter-sm">
          <UsageRing
            :label="t('gpuCoreUsage')"
            :value="device.usagePercent"
            :free-threshold="freeThreshold"
            :mid-threshold="midThreshold"
            size="4.6rem"
          />
          <UsageRing
            :label="t('gpuMemoryUsage')"
            :value="device.memoryUsagePercent"
            :free-threshold="freeThreshold"
            :mid-threshold="midThreshold"
            size="4.6rem"
          />
        </div>
        <div class="metric-facts q-mt-md">
          <div class="fact-row">
            <span>{{ t('gpuMemoryUsage') }}</span>
            <strong
              >{{ formatBytes(device.memory.usedBytes, unit) }} /
              {{ formatBytes(device.memory.totalBytes, unit) }}</strong
            >
          </div>
          <div class="fact-row">
            <span>{{ t('currentTemperature') }}</span>
            <strong>{{
              formatTemperature(device.temperatureCelsius, fahrenheit)
            }}</strong>
          </div>
          <div class="fact-row">
            <span>{{ t('power') }}</span>
            <strong>{{
              device.powerWatts == null
                ? '—'
                : `${rounded(device.powerWatts, 1)} W`
            }}</strong>
          </div>
          <div class="fact-row">
            <span>{{ t('fanSpeed') }}</span>
            <strong>{{
              device.fanSpeedPercent == null
                ? '—'
                : `${device.fanSpeedPercent}%`
            }}</strong>
          </div>
        </div>
      </section>
      <ProcessTable :rows="processes" metric="gpu" />
    </template>
    <div v-else class="empty-state text-muted-color">
      <q-icon name="mdi-expansion-card-off" size="md" />
      <span>{{ gpu.reason || t('noGpuData') }}</span>
    </div>
  </MetricCard>
</template>

<style scoped lang="scss">
.gpu-device + .gpu-device {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}
</style>
