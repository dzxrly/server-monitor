<script setup lang="ts">
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import UsageRing from '@/features/monitoring/components/shared/UsageRing.vue';
import type { ByteUnit } from '@/features/settings/model/config';
import { formatBytes } from '@/shared/format/metrics';

defineProps<{
  memory: MetricsSnapshot['memory'];
  unit: ByteUnit;
  freeThreshold: number;
  midThreshold: number;
}>();

const { t } = useI18n();
</script>

<template>
  <MetricCard
    class="detail-card"
    icon="fa-solid fa-memory"
    :title="t('memoryAndSwap')"
  >
    <div class="row justify-around q-gutter-md">
      <UsageRing
        :label="t('memoryUsage')"
        :value="memory.usagePercent"
        :free-threshold="freeThreshold"
        :mid-threshold="midThreshold"
        size="5rem"
      />
      <UsageRing
        :label="t('swapUsage')"
        :value="memory.swap.usagePercent"
        :free-threshold="freeThreshold"
        :mid-threshold="midThreshold"
        size="5rem"
      />
    </div>
    <div class="metric-facts q-mt-md">
      <div class="fact-row">
        <span>{{ t('memoryUsed') }}</span>
        <strong
          >{{ formatBytes(memory.usedBytes, unit) }} /
          {{ formatBytes(memory.totalBytes, unit) }}</strong
        >
      </div>
      <div class="fact-row">
        <span>{{ t('memoryAvailable') }}</span>
        <strong>{{ formatBytes(memory.availableBytes, unit) }}</strong>
      </div>
    </div>
  </MetricCard>
</template>
