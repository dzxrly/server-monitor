<script setup lang="ts">
import type { QTableColumn } from 'quasar';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import type { ProcessRow } from '@/features/monitoring/api/metrics-types';
import { formatBytes, rounded } from '@/shared/format/metrics';

const props = defineProps<{
  rows: ProcessRow[];
}>();

const { t } = useI18n();
const pagination = ref({
  sortBy: 'cpu',
  descending: true,
  page: 1,
  rowsPerPage: 0,
});
const columns = computed<QTableColumn<ProcessRow>[]>(() => [
  {
    name: 'process',
    label: t('process'),
    field: 'name',
    align: 'left',
    sortable: true,
    style: 'width: 42%',
    headerStyle: 'width: 42%',
  },
  {
    name: 'cpu',
    label: 'CPU',
    field: (row) => row.cpuUsagePercent ?? -1,
    align: 'right',
    sortable: true,
    style: 'width: 14%',
    headerStyle: 'width: 14%',
  },
  {
    name: 'memory',
    label: t('memory'),
    field: (row) => row.memoryBytes ?? -1,
    align: 'right',
    sortable: true,
    style: 'width: 22%',
    headerStyle: 'width: 22%',
  },
  {
    name: 'gpu',
    label: 'GPU',
    field: (row) => row.gpuUsagePercent ?? -1,
    align: 'right',
    sortable: true,
    style: 'width: 22%',
    headerStyle: 'width: 22%',
  },
]);

function formatPercent(value: number | null | undefined): string {
  return value == null ? '—' : `${rounded(value, 1)}%`;
}
</script>

<template>
  <q-table
    v-model:pagination="pagination"
    flat
    dense
    hide-bottom
    binary-state-sort
    row-key="pid"
    separator="horizontal"
    class="process-table bg-section-color text-card-color"
    table-header-class="text-muted-color"
    :rows="props.rows"
    :columns="columns"
    :rows-per-page-options="[0]"
    :no-data-label="t('noProcessData')"
  >
    <template #body-cell-process="slotProps">
      <q-td :props="slotProps" class="process-cell">
        <span class="process-name ellipsis block">{{
          slotProps.row.name
        }}</span>
        <span class="text-caption text-muted-color"
          >PID {{ slotProps.row.pid }}</span
        >
      </q-td>
    </template>

    <template #body-cell-cpu="slotProps">
      <q-td :props="slotProps" class="metric-cell">
        <strong>{{ formatPercent(slotProps.row.cpuUsagePercent) }}</strong>
      </q-td>
    </template>

    <template #body-cell-memory="slotProps">
      <q-td :props="slotProps" class="metric-cell">
        <strong>{{ formatBytes(slotProps.row.memoryBytes) }}</strong>
        <span class="metric-cell__secondary text-muted-color">
          {{ formatPercent(slotProps.row.memoryUsagePercent) }}
        </span>
      </q-td>
    </template>

    <template #body-cell-gpu="slotProps">
      <q-td :props="slotProps" class="metric-cell">
        <strong>{{ formatPercent(slotProps.row.gpuUsagePercent) }}</strong>
        <span class="metric-cell__secondary text-muted-color">
          {{ formatBytes(slotProps.row.gpuMemoryBytes) }}
        </span>
      </q-td>
    </template>
  </q-table>
</template>

<style scoped lang="scss">
.process-table {
  overflow: hidden;
  border: 0;
  border-radius: 12px;
  box-shadow: none;

  :deep(table) {
    table-layout: fixed;
  }

  :deep(th),
  :deep(td) {
    padding: 0.5rem 0.65rem;
  }
}

.process-cell,
.metric-cell {
  min-width: 0;
}

.process-name {
  font-weight: 500;
}

.metric-cell {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  strong,
  span {
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.metric-cell__secondary {
  font-size: 0.68rem;
}

@media (max-width: 600px) {
  .process-table {
    font-size: 0.76rem;

    :deep(th),
    :deep(td) {
      height: 2.8rem;
      padding: 0.4rem 0.3rem;
    }
  }

  .process-cell .text-caption,
  .metric-cell__secondary {
    font-size: 0.62rem;
  }
}
</style>
