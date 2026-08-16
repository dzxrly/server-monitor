<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import ProcessTable from '@/features/monitoring/components/shared/ProcessTable.vue';
import { mergeProcessRows } from '@/features/monitoring/model/process-rows';

const props = defineProps<{
  processes: MetricsSnapshot['processes'];
}>();

const { t } = useI18n();
const rows = computed(() => mergeProcessRows(props.processes));
</script>

<template>
  <MetricCard
    class="detail-card"
    icon="mdi-format-list-numbered"
    :title="t('processUsage')"
    :subtitle="t('processUsageSubtitle')"
  >
    <ProcessTable :rows="rows" />
  </MetricCard>
</template>
