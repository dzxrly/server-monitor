<script setup lang="ts">
import { computed, inject, PropType } from 'vue';
import { CPUCoreTemperature, CPUTemperature } from 'src/interface/api';
import { useI18n } from 'vue-i18n';
import { getDegreeUnit } from 'src/utils/utils';
import { QTableColumn } from 'quasar';

const props = defineProps({
  cpuTemperature: {
    type: Object as PropType<CPUTemperature>,
    required: true,
    default: () => {
      return {
        coresTemperature: [] as Array<CPUCoreTemperature>,
      } as CPUTemperature;
    },
  },
  useFahrenheit: {
    type: Boolean,
    default: false,
  },
});

const { t } = useI18n();

const isLtSm = inject('isLtSm', false);

const rowsPerPageOptions = computed(() => {
  if (
    props.cpuTemperature.coresTemperature &&
    typeof props.cpuTemperature.coresTemperature !== 'undefined'
  ) {
    const coreCount = props.cpuTemperature.coresTemperature.length;
    if (coreCount <= 32) {
      return [
        Math.floor(coreCount / 4),
        Math.floor(coreCount / 2),
        coreCount,
        0,
      ];
    } else if (coreCount > 32 && coreCount <= 64) {
      return [
        Math.floor(coreCount / 8),
        Math.floor(coreCount / 4),
        Math.floor(coreCount / 2),
        coreCount,
        0,
      ];
    } else if (coreCount > 64 && coreCount <= 128) {
      return [
        Math.floor(coreCount / 16),
        Math.floor(coreCount / 8),
        Math.floor(coreCount / 4),
        Math.floor(coreCount / 2),
        coreCount,
        0,
      ];
    } else if (coreCount > 128 && coreCount <= 256) {
      return [
        Math.floor(coreCount / 32),
        Math.floor(coreCount / 16),
        Math.floor(coreCount / 8),
        Math.floor(coreCount / 4),
        Math.floor(coreCount / 2),
        coreCount,
        0,
      ];
    } else {
      return [
        Math.floor(coreCount / 64),
        Math.floor(coreCount / 32),
        Math.floor(coreCount / 16),
        Math.floor(coreCount / 8),
        Math.floor(coreCount / 4),
        Math.floor(coreCount / 2),
        coreCount,
        0,
      ];
    }
  } else return [4, 8, 16, 32, 64, 0];
});

const coreTemperature = computed(() => {
  if (
    props.cpuTemperature.coresTemperature &&
    typeof props.cpuTemperature.coresTemperature !== 'undefined'
  ) {
    let deepCopyTemp = JSON.parse(
      JSON.stringify(props.cpuTemperature.coresTemperature)
    );
    return deepCopyTemp.sort(
      (a: CPUCoreTemperature, b: CPUCoreTemperature) =>
        parseInt(a.coreLabel.split(' ')[1]) -
        parseInt(b.coreLabel.split(' ')[1])
    );
  } else {
    return [] as Array<CPUCoreTemperature>;
  }
});

const tableColumns = [
  {
    name: 'coreLabel',
    required: true,
    label: t('core'),
    align: 'center',
    field: (row: CPUCoreTemperature) => row.coreLabel,
    format: (val: string) => `${val}`,
  },
  {
    name: 'currentTemperature',
    required: true,
    label: t('currentTemperature'),
    align: 'center',
    field: (row: CPUCoreTemperature) => row.coreCurrent,
    format: (val: number) => `${val}${getDegreeUnit(props.useFahrenheit)}`,
  },
  {
    name: 'maxTemperature',
    required: true,
    label: t('maxTemperature'),
    align: 'center',
    field: (row: CPUCoreTemperature) => row.coreHigh,
    format: (val: number) => `${val}${getDegreeUnit(props.useFahrenheit)}`,
  },
  {
    name: 'criticalTemperature',
    required: true,
    label: t('criticalTemperature'),
    align: 'center',
    field: (row: CPUCoreTemperature) => row.coreCritical,
    format: (val: number) => `${val}${getDegreeUnit(props.useFahrenheit)}`,
  },
] as QTableColumn[];
</script>

<template>
  <div
    class="cpu-temperature-row-wrapper"
    :class="isLtSm ? 'q-px-sm q-pb-sm' : 'q-px-md q-px-md'"
  >
    <q-table
      :rows="coreTemperature"
      :columns="tableColumns"
      row-key="coreLabel"
      table-class="text-card-color bg-card-color"
      card-class="text-card-color bg-card-color rounded-borders"
      :dense="isLtSm"
      :rows-per-page-label="t('rowsPerPage')"
      :rows-per-page-options="rowsPerPageOptions"
      separator="none"
      bordered
      flat
      grid
    />
  </div>
</template>
