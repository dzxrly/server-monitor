<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import CpuUsageTile from '@/features/monitoring/components/detail/CpuUsageTile.vue';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import {
  formatCpuFrequency,
  formatTemperature,
  rounded,
  usageColor,
} from '@/shared/format/metrics';

const props = defineProps<{
  cpu: MetricsSnapshot['cpu'];
  fahrenheit: boolean;
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();
const packageTemperature = computed(() => {
  const values = props.cpu.temperatures.map((sensor) => sensor.currentCelsius);
  return values.length > 0 ? Math.max(...values) : null;
});

function frequencyForCore(index: number): number | null {
  return (
    props.cpu.frequency.perCoreCurrentMhz?.[index] ??
    props.cpu.frequency.currentMhz
  );
}
</script>

<template>
  <MetricCard
    class="detail-card detail-card-wide"
    icon="mdi-memory"
    :title="cpu.name"
    :subtitle="`${cpu.physicalCores ?? '—'}C / ${cpu.logicalCores ?? '—'}T`"
  >
    <div class="cpu-summary">
      <div class="cpu-summary__item">
        <span>{{ t('cpuUsage') }}</span>
        <q-badge
          class="cpu-summary__usage"
          :color="usageColor(cpu.usagePercent, freeThreshold, midThreshold)"
          text-color="white"
        >
          {{ rounded(cpu.usagePercent) }}%
        </q-badge>
      </div>
      <div class="cpu-summary__item">
        <span>{{ t('cpuFreq') }}</span>
        <strong>{{ formatCpuFrequency(cpu.frequency.currentMhz) }}</strong>
      </div>
      <div class="cpu-summary__item">
        <span>{{ t('cpuTemp') }}</span>
        <strong>{{ formatTemperature(packageTemperature, fahrenheit) }}</strong>
      </div>
    </div>

    <div class="cpu-grid-heading q-mt-md q-mb-xs">
      <span>{{ t('perCoreUsage') }}</span>
      <span>{{ t('usage') }} · {{ t('cpuFreq') }}</span>
    </div>
    <div class="core-grid">
      <CpuUsageTile
        v-for="(usage, index) in cpu.perCoreUsagePercent"
        :key="index"
        :index="index"
        :usage="usage"
        :frequency-mhz="frequencyForCore(index)"
        :free-threshold="freeThreshold"
        :mid-threshold="midThreshold"
      />
    </div>
  </MetricCard>
</template>

<style scoped lang="scss">
.core-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(4.75rem, 1fr));
  gap: 0.4rem;
}

.cpu-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.2rem;
  overflow: hidden;
  border-radius: 12px;
}

.cpu-summary__item {
  display: grid;
  gap: 0.15rem;
  min-width: 0;
  padding: 0.65rem 0.8rem;
  background: var(--bg-section-color);

  span {
    color: var(--text-muted-color);
    font-size: 0.72rem;
  }

  strong,
  .cpu-summary__usage {
    overflow: hidden;
    font-size: 1.05rem;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.cpu-summary__usage {
  align-self: center;
  justify-self: start;
  padding: 0.25rem 0.55rem;
  border-radius: 6px;
  font-weight: 700;
  line-height: 1.2;
}

.cpu-grid-heading {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  color: var(--text-muted-color);
  font-size: 0.75rem;

  span:last-child {
    text-align: right;
  }
}

@media (max-width: 420px) {
  .core-grid {
    grid-template-columns: repeat(auto-fill, minmax(4.25rem, 1fr));
  }

  .cpu-summary__item {
    padding-inline: 0.55rem;

    span {
      font-size: 0.66rem;
    }

    strong,
    .cpu-summary__usage {
      font-size: 0.9rem;
    }
  }
}
</style>
