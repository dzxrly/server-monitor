<template>
  <div
    class="cpu-temperature-row-wrapper"
    :class="isLtSm ? 'q-px-sm q-pb-sm' : 'q-px-md q-px-md'"
  >
    <q-table
      :rows="coreTemperature"
      :columns="tableColumns"
      row-key="coreLabel"
      :bordered="false"
      table-class="text-card-color bg-card-color"
      card-class="text-card-color bg-card-color"
      :dense="isLtSm"
      :rows-per-page-label="t('rowsPerPage')"
      flat
    />
  </div>
</template>

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
