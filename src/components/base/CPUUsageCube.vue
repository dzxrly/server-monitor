<script setup lang="ts">
import {computed} from 'vue';
import {getUsageColor, rounded} from 'src/utils/utils';

const props = defineProps({
  cpuUsage: {
    type: Number,
    default: 0,
  },
  cpuFreq: {
    type: Number,
    default: 0,
  },
  useFahrenheit: {
    type: Boolean,
    default: false,
  },
  cubeSize: {
    type: Number,
    default: 10,
  },
  textSizePercentage: {
    type: Number,
    default: 0.5,
    validator: (value: number) => value >= 0 && value <= 1,
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
  animationSpeedSec: {
    type: Number,
    default: 0.1
  }
});

const cubeSize = computed(() => {
  return `${props.cubeSize}rem`;
});

const textSize = computed(() => {
  return `${props.textSizePercentage * props.cubeSize}rem`;
});

const paddingSize = computed(() => {
  return `${(props.textSizePercentage * props.cubeSize) / 2}rem`;
});

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

const animationSpeed = computed(() => {
  return `${props.animationSpeedSec}s`
})
</script>

<template>
  <div
    class="cpu-usage-cube-wrapper column justify-center items-center no-wrap bg-transparent"
  >
    <div
      class="cpu-usage-text-wrapper text-default-color bg-default-color column justify-center items-center no-wrap"
    >
      <span>{{ `${rounded(props.cpuUsage, 0)}%` }}</span>
      <span v-if="props.cpuFreq > 0">{{
        `${rounded(props.cpuFreq / 1000, 1)}GHz`
      }}</span>
    </div>
  </div>
</template>

<style lang="sass" scoped>
.cpu-usage-cube-wrapper
  position: relative
  width: v-bind(cubeSize)
  height: v-bind(cubeSize)
  border: solid 1px $primary
  box-sizing: border-box
  border-radius: v-bind(paddingSize)
  overflow: hidden
  z-index: 0

  .cpu-usage-text-wrapper
    font-size: v-bind(textSize)
    padding: 0 v-bind(paddingSize)
    border-radius: v-bind(paddingSize)
    z-index: 2

.cpu-usage-cube-wrapper::before
  content: ''
  position: absolute
  width: v-bind(cubeSize)
  height: v-bind(cubeSize)
  background-color: v-bind(bgColor)
  transform: v-bind(cpuUsageTranslateY)
  transition: all v-bind(animationSpeed) linear
  z-index: 1
</style>
