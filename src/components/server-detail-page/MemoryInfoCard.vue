<script setup lang="ts">
import {MemoryStateResponse} from 'src/interface/api';
import {PropType} from 'vue';
import {useConfigStore} from 'stores/user-config';
import {useI18n} from 'vue-i18n';
import {ByteUnit} from 'src/module/config';
import MemoryInfoRow from "components/base/MemoryInfoRow.vue";

const props = defineProps({
  memoryState: {
    type: Object as PropType<MemoryStateResponse>,
    required: true,
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

const configStore = useConfigStore();
const { t } = useI18n();
</script>

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
    <MemoryInfoRow
      class="q-mt-md"
      :memory-state="props.memoryState"
      :free-usage-threshold="configStore.config.freeUsageThreshold"
      :mid-usage-threshold="configStore.config.midUsageThreshold"
      :memory-unit="configStore.config.memoryUnit"
      :animation-speed-sec="props.animationSpeedSec"
    />
  </div>
</template>
