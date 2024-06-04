<template>
  <div
    class="clickable-select-row-wrapper q-px-md full-width bg-transparent">
    <div v-if="!isLtSm" class="row justify-between items-center no-wrap">
      <span class="text-base-color text-subtitle1 col-6">{{ props.title }}</span>
      <q-select
        class="col-6"
        v-model="selectValue"
        :options="props.options"
        color="primary"
        size="md"
        emit-value
        outlined
        map-options
        dense
      />
    </div>
    <q-select
      v-else
      class="full-width"
      v-model="selectValue"
      :options="props.options"
      :label="props.title"
      color="primary"
      size="md"
      emit-value
      outlined
      map-options
    />
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue';

const selectValue = defineModel('selectValue', { required: true, type: String });

const props = defineProps({
  title: { required: true, type: String },
  options: {
    required: true, type: Array<{
      value: string | number,
      label: string,
    }>
  }
});

const isLtSm = inject('isLtSm');
</script>
