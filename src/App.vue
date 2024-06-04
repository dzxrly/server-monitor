<template>
  <router-view />
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { computed, onMounted, provide } from 'vue';
import { useUserConfigStore } from 'stores/user-config';
import { useI18n } from 'vue-i18n';

const $q = useQuasar();
const userConfigStore = useUserConfigStore();
const { locale } = useI18n({ useScope: 'global' });

const darkMode = computed(() => userConfigStore.getUserConfig.userConfig.darkMode);
const defaultLanguage = computed(() => userConfigStore.getUserConfig.userConfig.defaultLanguage);
const isLtSm = computed(() => $q.screen.lt.sm);

provide('isLtSm', isLtSm);
provide('darkMode', darkMode);

userConfigStore.initUserConfigFromLocalStorage();

onMounted(() => {
  // set language by defaultLanguage
  locale.value = defaultLanguage.value;
});
</script>
