<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { ProcessRow } from '@/features/monitoring/api/metrics-types';
import { formatBytes, rounded } from '@/shared/format/metrics';

const props = defineProps<{
  rows: ProcessRow[];
  metric: 'cpu' | 'memory' | 'gpu';
}>();

const { t } = useI18n();
const heading = computed(() => {
  if (props.metric === 'cpu') return t('topCpuProcesses');
  if (props.metric === 'memory') return t('topMemoryProcesses');
  return t('topGpuProcesses');
});

function value(row: ProcessRow): string {
  if (props.metric === 'cpu') return `${rounded(row.cpuUsagePercent, 1)}%`;
  if (props.metric === 'memory') {
    return `${formatBytes(row.memoryBytes)} · ${rounded(row.memoryUsagePercent, 1)}%`;
  }
  const usage =
    row.gpuUsagePercent == null ? '' : `${rounded(row.gpuUsagePercent, 1)}% · `;
  return `${usage}${formatBytes(row.gpuMemoryBytes)}`;
}
</script>

<template>
  <div class="q-mt-md">
    <div class="text-caption text-muted-color q-mb-xs">{{ heading }}</div>
    <q-markup-table
      flat
      dense
      class="process-table bg-transparent text-card-color"
    >
      <thead>
        <tr>
          <th class="text-left">{{ t('process') }}</th>
          <th class="text-right">{{ t('usage') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.pid">
          <td class="text-left process-name">
            <span class="ellipsis block">{{ row.name }}</span>
            <span class="text-caption text-muted-color">PID {{ row.pid }}</span>
          </td>
          <td class="text-right no-wrap">{{ value(row) }}</td>
        </tr>
        <tr v-if="rows.length === 0">
          <td colspan="2" class="text-center text-muted-color q-py-sm">
            {{ t('noProcessData') }}
          </td>
        </tr>
      </tbody>
    </q-markup-table>
  </div>
</template>

<style scoped lang="scss">
.process-table {
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
}

.process-name {
  max-width: 14rem;
}
</style>
