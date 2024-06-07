<template>
  <div
    class="cpu-usage-cube-wrapper column justify-center items-center no-wrap bg-transparent"
  ></div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { getUsageColor } from 'src/utils/utils';

const props = defineProps({
  cpuUsage: {
    type: Number,
    default: 0
  },
  cpuTemperature: {
    type: Number,
    default: 0
  },
  useFahrenheit: {
    type: Boolean,
    default: false
  },
  cubeSize: {
    type: String,
    default: '10rem'
  },
  textSizePercentage: {
    type: Number,
    default: 0.5,
    validator: (value: number) => value >= 0 && value <= 1
  },
  freeUsageThreshold: {
    type: Number,
    default: 20,
    validator(val: number) {
      return val >= 0 && val <= 100;
    }
  },
  midUsageThreshold: {
    type: Number,
    default: 60,
    validator(val: number) {
      return val >= 0 && val <= 100;
    }
  }
});

const cubeSize = ref(props.cubeSize);

const bgColor = computed(() => {
  return getUsageColor(
    props.cpuUsage,
    props.freeUsageThreshold,
    props.midUsageThreshold
  );
});
const cpuUsageTranslateY = computed(() => {
  if (100 - props.cpuUsage <= 0) {
    return 'translateY(1%)';
  } else if (100 - props.cpuUsage >= 100) {
    return 'translateY(100%)';
  } else {
    return `translateY(${100 - props.cpuUsage}%)`;
  }
});
</script>

<style lang="sass" scoped>
.cpu-usage-cube-wrapper
  position: relative
  width: v-bind(cubeSize)
  height: v-bind(cubeSize)
  border: solid 1px $primary
  box-sizing: content-box
  overflow: hidden

.cpu-usage-cube-wrapper::before
  content: ''
  position: absolute
  width: v-bind(cubeSize)
  height: v-bind(cubeSize)
  background-color: v-bind(bgColor)
  transform: v-bind(cpuUsageTranslateY)
  transition: all 0.1s linear
  z-index: 9999
</style>
