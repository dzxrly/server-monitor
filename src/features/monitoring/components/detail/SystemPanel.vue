<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import { formatUptime } from '@/shared/format/metrics';

const props = defineProps<{ system: MetricsSnapshot['system'] }>();
const { t } = useI18n();
const icon = computed(() => {
  const platform = props.system.platform.toLowerCase();
  if (platform.includes('windows')) return 'fa-brands fa-windows';
  if (platform.includes('linux')) return 'fa-brands fa-linux';
  return 'desktop_windows';
});
</script>

<template>
  <MetricCard class="detail-card" :icon="icon" :title="t('osCardTitle')">
    <div class="metric-facts">
      <div class="fact-row">
        <span>{{ t('osNameTitle') }}</span
        ><strong>{{ system.name }}</strong>
      </div>
      <div class="fact-row">
        <span>{{ t('osVersion') }}</span
        ><strong>{{ system.version }}</strong>
      </div>
      <div class="fact-row">
        <span>{{ t('deviceNameTitle') }}</span
        ><strong>{{ system.hostname }}</strong>
      </div>
      <div class="fact-row">
        <span>{{ t('osArchitectureTitle') }}</span
        ><strong>{{ system.architecture }} · {{ system.bits }}</strong>
      </div>
      <div class="fact-row">
        <span>{{ t('osKernel') }}</span
        ><strong>{{ system.kernel }}</strong>
      </div>
      <div class="fact-row">
        <span>{{ t('uptime') }}</span
        ><strong>{{ formatUptime(system.uptimeSeconds) }}</strong>
      </div>
    </div>
  </MetricCard>
</template>
