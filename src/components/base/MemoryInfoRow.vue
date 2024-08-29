<script setup lang="ts">
import {useI18n} from "vue-i18n";
import {ByteUnit} from "src/module/config";
import {PropType} from "vue";
import {MemoryStateResponse} from "src/interface/api";
import {getUsageColorClass, rounded} from "src/utils/utils";

const props = defineProps({
  memoryState: {
    type: Object as PropType<MemoryStateResponse>,
    required: true,
  },
  freeUsageThreshold: {
    type: Number,
    default: 20,
    validator(val: number) {
      return val >= 0 && val <= 100;
    },
  },
  midUsageThreshold: {
    type: Number,
    default: 60,
    validator(val: number) {
      return val >= 0 && val <= 100;
    },
  },
  memoryUnit: {
    type: String,
    default: ByteUnit.GB,
  },
  animationSpeedSec: {
    type: Number,
    default: 0.1
  }
});

const {t} = useI18n();
</script>

<template>
  <div class="ram-info-row-wrapper column justify-between items-center full-width no-wrap">
    <div class="row justify-between items-center full-width no-wrap">
      <span class="col-4 text-card-color text-body2">{{
          t('memoryUsage')
        }}</span>
      <q-linear-progress
        class="col-grow q-ml-xs rounded-borders"
        :value="props.memoryState.memoryPercent / 100"
        :class="
          getUsageColorClass(
            props.memoryState.memoryPercent,
            props.freeUsageThreshold,
            props.midUsageThreshold
          )
        "
        track-color="grey-6"
        size="1.2rem"
        :animation-speed="props.animationSpeedSec * 1000"
      >
        <div class="absolute-full flex flex-center">
          <q-badge
            color="default-color"
            class="text-card-color"
            :label="`${rounded(props.memoryState.memoryUsed, 2)}/${rounded(
              props.memoryState.memoryTotal,
              2
            )} ${props.memoryUnit}`"
          />
        </div>
      </q-linear-progress>
    </div>
    <div class="row justify-between items-center full-width no-wrap q-mt-sm">
      <span class="col-4 text-card-color text-body2">{{ t('swapUsage') }}</span>
      <q-linear-progress
        class="col-grow q-ml-xs rounded-borders"
        :value="props.memoryState?.swapPercent / 100"
        :class="
          getUsageColorClass(
            props.memoryState?.swapPercent,
            props.freeUsageThreshold,
            props.midUsageThreshold
          )
        "
        track-color="grey-6"
        size="1.2rem"
        :animation-speed="props.animationSpeedSec * 1000"
      >
        <div class="absolute-full flex flex-center">
          <q-badge
            color="default-color"
            class="text-card-color"
            :label="`${rounded(props.memoryState?.swapUsed, 2)}/${rounded(
              props.memoryState?.swapTotal,
              2
            )} ${props.memoryUnit}`"
          />
        </div>
      </q-linear-progress>
    </div>
  </div>
</template>

<style scoped lang="sass">

</style>
