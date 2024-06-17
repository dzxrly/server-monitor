<template>
  <div
    class="memory-info-card-wrapper bg-card-color full-width column justify-center items-center no-wrap rounded-borders q-pa-md"
  >
    <div class="row justify-between items-center full-width no-wrap">
      <div class="row justify-start items-center full-width no-wrap">
        <q-icon class="q-mr-xs" name="fa-solid fa-memory" size="xs" />
        <span class="text-card-color text-subtitle2 overflow-hidden ellipsis">{{
          t('memoryAndSwap')
        }}</span>
      </div>
    </div>
    <div class="row justify-between items-center full-width no-wrap q-mt-md">
      <span class="col-4 text-card-color text-body2">{{
        t('memoryUsage')
      }}</span>
      <q-linear-progress
        class="col-grow q-ml-xs rounded-borders"
        :value="props.memoryState.memoryPercent / 100"
        :class="
          getUsageColorClass(
            props.memoryState.memoryPercent,
            configStore.config.freeUsageThreshold,
            configStore.config.midUsageThreshold
          )
        "
        track-color="grey-6"
        size="1.2rem"
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
            configStore.config.freeUsageThreshold,
            configStore.config.midUsageThreshold
          )
        "
        track-color="grey-6"
        size="1.2rem"
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

<script setup lang="ts">
import { MemoryStateResponse } from 'src/interface/api';
import { PropType } from 'vue';
import { useConfigStore } from 'stores/user-config';
import { useI18n } from 'vue-i18n';
import { getUsageColorClass, rounded } from 'src/utils/utils';
import { ByteUnit } from 'src/module/config';

const props = defineProps({
  memoryState: {
    type: Object as PropType<MemoryStateResponse>,
    required: true,
  },
  memoryUnit: {
    type: String,
    default: ByteUnit.GB,
  },
});

const configStore = useConfigStore();
const { t } = useI18n();
</script>
