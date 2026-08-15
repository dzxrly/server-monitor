<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import ProcessTable from '@/features/monitoring/components/shared/ProcessTable.vue';
import UsageRing from '@/features/monitoring/components/shared/UsageRing.vue';
import {
  formatTemperature,
  rounded,
  usageColor,
} from '@/shared/format/metrics';

const props = defineProps<{
  cpu: MetricsSnapshot['cpu'];
  processes: MetricsSnapshot['processes']['cpu'];
  fahrenheit: boolean;
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();
const packageTemperature = computed(() => {
  const values = props.cpu.temperatures.map((sensor) => sensor.currentCelsius);
  return values.length > 0 ? Math.max(...values) : null;
});
</script>

<template>
  <MetricCard
    class="detail-card detail-card-wide"
    icon="mdi-memory"
    :title="cpu.name"
    :subtitle="`${cpu.physicalCores ?? '—'}C / ${cpu.logicalCores ?? '—'}T`"
  >
    <div class="row items-center q-col-gutter-md">
      <div class="col-auto">
        <UsageRing
          :label="t('cpuUsage')"
          :value="cpu.usagePercent"
          :free-threshold="freeThreshold"
          :mid-threshold="midThreshold"
          size="5.25rem"
        />
      </div>
      <div class="col metric-facts">
        <div class="fact-row">
          <span>{{ t('cpuFreq') }}</span>
          <strong>{{ rounded(cpu.frequency.currentMhz, 0) }} MHz</strong>
        </div>
        <div class="fact-row">
          <span>{{ t('cpuTemp') }}</span>
          <strong>{{
            formatTemperature(packageTemperature, fahrenheit)
          }}</strong>
        </div>
      </div>
    </div>

    <div class="text-caption text-muted-color q-mt-md q-mb-xs">
      {{ t('perCoreUsage') }}
    </div>
    <div class="core-grid">
      <div
        v-for="(usage, index) in cpu.perCoreUsagePercent"
        :key="index"
        class="core-cell"
      >
        <div class="row justify-between text-caption q-mb-xs">
          <span>#{{ index + 1 }}</span
          ><span>{{ rounded(usage) }}%</span>
        </div>
        <q-linear-progress
          rounded
          :value="usage / 100"
          :color="usageColor(usage, freeThreshold, midThreshold)"
          track-color="progress-track"
          size="6px"
        />
      </div>
    </div>
    <ProcessTable :rows="processes" metric="cpu" />
  </MetricCard>
</template>

<style scoped lang="scss">
.core-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(5.5rem, 1fr));
  gap: 0.45rem;
}

.core-cell {
  padding: 0.45rem 0.55rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
}

.metric-facts {
  min-width: 10rem;
}
</style>
