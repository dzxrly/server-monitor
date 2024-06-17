<template>
  <div
    class="circular-progress-whit-title-wrapper column justify-center items-center full-width"
  >
    <span
      v-if="props.title && props.title !== ''"
      class="text-subtitle2 text-card-color"
      >{{ props.title }}</span
    >
    <div
      v-if="!isError"
      :class="{ 'q-mt-xs': props.title && props.title !== '' }"
    >
      <q-circular-progress
        show-value
        :value="value"
        :size="progressSize"
        :class="props.color"
        :thickness="props.size * 0.05"
        track-color="grey-6"
      >
        <span class="inner-text-span text-card-color">{{
          props.showValueText
        }}</span>
      </q-circular-progress>
    </div>
    <div
      v-else
      class="column justify-center items-center no-wrap full-width q-mt-xs"
    >
      <q-icon name="error" size="md" color="negative" />
      <span class="text-card-color q-mt-sm">{{ t('loadingFailed') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  value: {
    type: Number,
    required: true,
  },
  showValueText: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    default: 'primary',
  },
  isError: {
    type: Boolean,
    default: false,
  },
  size: {
    type: Number,
    default: 4,
  },
  innerTextSizePercentage: {
    type: Number,
    default: 0.2,
    validator: (value: number) => {
      return value >= 0 && value <= 1;
    },
  },
});

const { t } = useI18n();

const progressSize = computed(() => {
  return `${props.size}rem`;
});

const innerTextSize = computed(() => {
  return `${props.size * props.innerTextSizePercentage}rem`;
});
</script>

<style lang="sass" scoped>
.circular-progress-whit-title-wrapper
  .inner-text-span
    font-size: v-bind(innerTextSize) !important
</style>
