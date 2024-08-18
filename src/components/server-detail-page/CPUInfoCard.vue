<script setup lang="ts">
import { getDegreeUnit, rounded } from 'src/utils/utils';
import CPUTemperatureRow from 'components/base/CPUTemperatureRow.vue';
import CPUUsageCube from 'components/base/CPUUsageCube.vue';
import { CPUNameResponse, CPUStatePerCPUResponse } from 'src/interface/api';
import { computed, inject, PropType } from 'vue';
import { useI18n } from 'vue-i18n';
import { useConfigStore } from 'stores/user-config';

const props = defineProps({
  cpuState: {
    type: Object as PropType<CPUStatePerCPUResponse>,
    required: true,
  },
  cpuName: {
    type: Object as PropType<CPUNameResponse>,
    required: true,
  },
  cpuUsageCubeSize: {
    type: Number,
    required: true,
  },
  cpuUsageInnerTextPercentage: {
    type: Number,
    required: true,
  },
});

const { t } = useI18n();
const configStore = useConfigStore();

const isLtSm = inject('isLtSm', false);

const cpuUsageCubeGridSizeComputed = computed(() => {
  return `${props.cpuUsageCubeSize}rem`;
});
</script>

<template>
  <div
    class="cpu-info-card-wrapper bg-card-color full-width column justify-center items-center no-wrap rounded-borders q-pa-md"
  >
    <div class="row justify-between items-center wrap full-width">
      <div>
        <q-icon
          class="q-mr-xs"
          name="mdi-memory"
          :size="isLtSm ? 'xs' : 'md'"
        />
        <span
          class="text-card-color text-subtitle2 overflow-hidden ellipsis q-mr-xs"
          >{{
            props.cpuName?.cpuName.split('@')[0].trim().split('CPU')[0].trim()
          }}</span
        >
        <q-badge
          v-if="
            props.cpuState?.cpuTemperature &&
            props.cpuState?.cpuTemperature.length >= 2
          "
          class="text-card-color text-subtitle2 cursor-pointer"
          rounded
          color="default-color"
        >
          ×{{ props.cpuState.cpuTemperature.length }}
          <q-tooltip>
            {{ t('numaNode') }}
          </q-tooltip>
        </q-badge>
      </div>
      <span class="text-card-color text-caption">{{
        `${props.cpuState?.cpuCores.cores}C${props.cpuState?.cpuCores.threads}T`
      }}</span>
    </div>
    <div class="row justify-start items-center no-wrap full-width q-mt-md">
      <span class="text-card-color text-body2">{{ t('cpuUsage') }}</span>
    </div>
    <div class="cpu-usage-cube-wrapper full-width q-mt-sm">
      <CPUUsageCube
        v-for="(core, index) of props.cpuState?.cpuUsage.percpu"
        :key="index"
        :cpu-usage="core"
        :cpu-freq="
          props.cpuState &&
          props.cpuState.cpuFreq &&
          props.cpuState.cpuFreq.percpu &&
          props.cpuState.cpuFreq.percpu[index]
            ? props.cpuState.cpuFreq.percpu[index].current
            : -1
        "
        :use-fahrenheit="configStore.config.useFahrenheitUnit"
        :cube-size="props.cpuUsageCubeSize"
        :text-size-percentage="props.cpuUsageInnerTextPercentage"
        :free-usage-threshold="configStore.config.freeUsageThreshold"
        :mid-usage-threshold="configStore.config.midUsageThreshold"
      />
    </div>
    <div
      v-if="
        props.cpuState?.cpuTemperature &&
        props.cpuState?.cpuTemperature.length > 0
      "
      class="row justify-start items-center no-wrap full-width q-mt-md"
    >
      <span class="text-card-color text-body2">{{ t('cpuTemp') }}</span>
    </div>
    <div
      v-if="
        props.cpuState?.cpuTemperature &&
        props.cpuState?.cpuTemperature.length > 0
      "
      class="column justify-center items-center full-width q-mt-sm"
    >
      <q-expansion-item
        class="full-width"
        v-for="(cpuTemp, index) of props.cpuState.cpuTemperature"
        :key="cpuTemp.numaLabel ?? index"
        switch-toggle-side
      >
        <template v-slot:header>
          <div
            class="row justify-between items-center no-wrap full-width text-card-color text-body2"
          >
            <span>{{ `CPU ${index}` }}</span>
            <div class="row justify-center items-center no-wrap">
              <q-icon name="mdi-thermometer" size="xs" />
              <span class="q-pl-xs">{{
                `${rounded(cpuTemp.numaCurrent ?? 0, 2)}${getDegreeUnit(
                  configStore.config.useFahrenheitUnit
                )}`
              }}</span>
            </div>
          </div>
        </template>
        <template v-slot:default>
          <CPUTemperatureRow :cpu-temperature="cpuTemp" />
        </template>
      </q-expansion-item>
    </div>
  </div>
</template>

<style scoped lang="sass">
.cpu-info-card-wrapper
  .cpu-usage-cube-wrapper
    display: grid
    grid-template-rows: repeat(auto-fill, v-bind(cpuUsageCubeGridSizeComputed))
    grid-template-columns: repeat(auto-fill, v-bind(cpuUsageCubeGridSizeComputed))
    justify-items: center
    align-items: center
    justify-content: center
    align-content: center
    grid-gap: 0.1rem
</style>
