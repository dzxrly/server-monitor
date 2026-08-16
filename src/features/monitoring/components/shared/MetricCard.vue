<script setup lang="ts">
defineProps<{
  title: string;
  icon: string;
  subtitle?: string;
}>();
</script>

<template>
  <q-card
    flat
    class="metric-card bg-card-color text-card-color rounded-borders"
  >
    <q-card-section class="q-pa-md">
      <header class="row items-center no-wrap q-mb-md">
        <q-icon :name="icon" size="sm" class="q-mr-sm" />
        <div class="col min-width-zero">
          <div class="text-subtitle1 text-weight-medium ellipsis">
            {{ title }}
          </div>
          <div v-if="subtitle" class="text-caption text-muted-color ellipsis">
            {{ subtitle }}
          </div>
        </div>
        <slot name="action" />
      </header>
      <slot />
    </q-card-section>
  </q-card>
</template>

<style scoped lang="scss">
.metric-card {
  height: 100%;
  border: 0;
  box-shadow: none;
  transition: background-color 0.2s ease;
}

.min-width-zero {
  min-width: 0;
}
</style>
