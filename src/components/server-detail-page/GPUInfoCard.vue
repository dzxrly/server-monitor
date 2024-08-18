<script setup lang="ts">
import GPUInfoRow from 'components/base/GPUInfoRow.vue';
import { PropType } from 'vue';
import { GPUStateResponse } from 'src/interface/api';
import { ByteUnit } from 'src/module/config';

const props = defineProps({
  gpuState: {
    type: Object as PropType<GPUStateResponse>,
    required: true,
  },
  isError: {
    type: Boolean,
    default: false,
  },
  useFahrenheitUnit: {
    type: Boolean,
    default: false,
  },
  gpuMemoryUnit: {
    type: String,
    default: ByteUnit.GB,
  },
});
</script>

<template>
  <div
    class="gpu-info-card-wrapper bg-card-color full-width column justify-center items-center no-wrap rounded-borders q-pa-md"
  >
    <GPUInfoRow
      :gpu-state="props.gpuState"
      :is-error="props.isError"
      :use-fahrenheit-unit="props.useFahrenheitUnit"
      :gpu-memory-unit="props.gpuMemoryUnit"
      show-layout="lg"
    />
  </div>
</template>
