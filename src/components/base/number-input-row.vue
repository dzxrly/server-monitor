<template>
  <div class="number-input-row-wrapper q-px-md full-width bg-transparent">
    <div v-if="!isLtSm" class="row justify-between items-center no-wrap">
      <span class="text-base-color text-subtitle1 col-6">{{ props.title }}</span>
      <q-input
        class="col-6"
        v-model.number="value"
        type="number"
        color="primary"
        outlined
        dense
        :max="props.max"
        :min="props.min"
        :step="props.step"
      />
    </div>
    <q-input
      v-else
      class="full-width"
      v-model.number="value"
      type="number"
      :label="props.title"
      color="primary"
      outlined
      dense
      :max="props.max"
      :min="props.min"
      :step="props.step"
    />
  </div>
</template>

<script setup lang="ts">
import { inject, watch } from 'vue';

const value = defineModel('value', { required: true, type: Number });

const props = defineProps({
  title: { required: true, type: String },
  max: { required: false, type: Number, default: 100 },
  min: { required: false, type: Number, default: 0 },
  step: { required: false, type: Number, default: 1 }
});

const isLtSm = inject('isLtSm');

watch(value, (newVal: string | number) => {
  if (newVal < props.min) {
    value.value = props.min;
  } else if (newVal > props.max) {
    value.value = props.max;
  } else {
    value.value = newVal as number;
  }
});
</script>
