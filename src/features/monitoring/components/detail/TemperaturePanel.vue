<script setup lang="ts">
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import { formatTemperature } from '@/shared/format/metrics';

defineProps<{
  temperatures: MetricsSnapshot['temperatures'];
  fahrenheit: boolean;
}>();

const { t } = useI18n();
</script>

<template>
  <MetricCard
    class="detail-card"
    icon="mdi-thermometer"
    :title="t('hardwareTemperatures')"
    :subtitle="temperatures.provider"
  >
    <div v-if="temperatures.sensors.length > 0" class="sensor-list">
      <div
        v-for="sensor in temperatures.sensors"
        :key="sensor.identifier || `${sensor.hardware}-${sensor.name}`"
        class="sensor-row"
      >
        <div class="col min-width-zero">
          <div class="ellipsis">{{ sensor.name }}</div>
          <div class="text-caption text-muted-color ellipsis">
            {{ sensor.hardware }}
          </div>
        </div>
        <strong>{{
          formatTemperature(sensor.currentCelsius, fahrenheit)
        }}</strong>
      </div>
    </div>
    <div v-else class="empty-state text-muted-color">
      <q-icon name="mdi-thermometer-off" size="md" />
      <span>{{ temperatures.reason || t('noTemperatureData') }}</span>
    </div>
  </MetricCard>
</template>

<style scoped lang="scss">
.sensor-list {
  display: grid;
  gap: 0.5rem;
}

.sensor-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.55rem 0.65rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
}

.min-width-zero {
  min-width: 0;
}
</style>
