<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  fanSpeed: {
    type: Number,
    required: true,
    default: 0,
  },
  size: {
    type: String,
    default: '0.8rem',
  },
  functionCoeffA: {
    type: Number,
    default: -0.019,
  },
  functionCoeffB: {
    type: Number,
    default: 2,
  },
});

const fanSpeed = computed(() => {
  return `${props.functionCoeffA * props.fanSpeed + props.functionCoeffB}s`;
});
</script>

<template>
  <div class="fan-icon-wrapper text-base-color">
    <q-icon class="fan-icon" name="mdi-fan" :size="props.size" />
  </div>
</template>

<style scoped lang="sass">
.fan-icon-wrapper
  --rotate-time: v-bind(fanSpeed)

  .fan-icon
    transform-origin: center
    animation: infinite var(--rotate-time) fan-spin linear

    @keyframes fan-spin
      0%
        transform: rotate(0deg)
      100%
        transform: rotate(360deg)
</style>
