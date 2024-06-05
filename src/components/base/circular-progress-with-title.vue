<template>
  <div class="circular-progress-whit-title-wrapper column justify-center items-center full-width">
    <span class="text-subtitle2 text-base-color">{{ props.title }}</span>
    <div v-if="!isError" class="q-mt-xs">
      <q-circular-progress
        show-value
        :value="value"
        size="xl"
        :class="props.color"
        track-color="grey-6"
      >
        <span class="text-base-color">{{ props.value }}%</span>
      </q-circular-progress>
    </div>
    <div v-else class="column justify-center items-center no-wrap full-width q-mt-xs">
      <q-icon name="error" size="md" color="negative" />
      <span class="text-base-color q-mt-sm">{{ t('loadingFailed') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">

import { useI18n } from 'vue-i18n';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: Number,
    required: true
  },
  color: {
    type: String,
    default: 'primary'
  },
  isError: {
    type: Boolean,
    default: false
  }
});

const { t } = useI18n();
</script>
