<script setup lang="ts">
import { watch } from 'vue';
import { useI18n } from 'vue-i18n';

import { useConfigStore } from '@/features/settings/stores/config-store';

const configStore = useConfigStore();
const { locale } = useI18n({ useScope: 'global' });

watch(
  () => configStore.config.defaultLanguage,
  (language) => {
    locale.value = language;
  },
  { immediate: true },
);
</script>

<template>
  <router-view />
</template>
