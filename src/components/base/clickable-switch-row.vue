<template>
  <div class="clickable-switch-row-wrapper full-width bg-transparent">
    <label class="clickable-switch-row row justify-between items-center no-wrap cursor-pointer q-px-md">
      <span class="text-base-color text-subtitle1">{{ props.title }}</span>
      <q-toggle
        v-model="switchValue"
        color="primary"
        size="md" />
    </label>
  </div>
</template>

<script setup lang="ts">
const switchValue = defineModel('switchValue', { required: true, type: Boolean });
const props = defineProps({
  title: { required: true, type: String }
});
</script>

<style scoped lang="sass">
.clickable-switch-row-wrapper
  user-select: none

  .clickable-switch-row
    transition: all 0.3s ease-in-out

  .clickable-switch-row:hover
    background-color: rgba(0, 0, 0, 0.1)
</style>
