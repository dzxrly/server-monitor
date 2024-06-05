<template>
  <router-view />
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { computed, onMounted, provide } from 'vue';
import { useConfigStore } from 'stores/user-config';
import { useI18n } from 'vue-i18n';

const $q = useQuasar();
const configStore = useConfigStore();
const { locale } = useI18n({ useScope: 'global' });

configStore.initConfig();

const darkMode = computed(() => configStore.config.userConfig.darkMode);
const defaultLanguage = computed(() => configStore.config.userConfig.defaultLanguage);
const isLtSm = computed(() => $q.screen.lt.sm);

provide('isLtSm', isLtSm);
provide('darkMode', darkMode);

onMounted(() => {
  // set language by defaultLanguage
  locale.value = defaultLanguage.value;
});
</script>
