<template>
  <div
    class="setting-dialog-wrapper column justify-center items-center no-wrap full-width bg-card-color rounded-borders q-pa-md">
    <div class="row justify-between items-center full-width">
      <span class="text-base-color text-h6">{{ t('settings') }}</span>
      <q-btn
        icon="close"
        class="text-base-color"
        @click="showSettingDialog = false"
        round
        flat
      />
    </div>
    <ClickableSwitchRow
      class="q-mt-md"
      v-model:switch-value="userConfig.darkMode"
      :title="t('darkMode')"
    />
    <ClickableSwitchRow
      v-model:switch-value="userConfig.useFahrenheitUnit"
      :title="t('useFahrenheitUnit')"
    />
    <ClickableSelectRow
      class="q-mt-sm"
      v-model:select-value="userConfig.indexPageServerPanelLayout"
      :title="t('indexPageServerPanelLayout')"
      :options="layoutSettingOptions"
    />
    <ClickableSelectRow
      class="q-mt-sm"
      v-model:select-value="userConfig.defaultLanguage"
      :title="t('language')"
      :options="langSettingOptions"
      v-on:update:select-value="(val) => locale = val"
    />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ClickableSwitchRow from 'components/base/clickable-switch-row.vue';
import { useUserConfigStore } from 'stores/user-config';
import { reactive, watch } from 'vue';
import ClickableSelectRow from 'components/base/clickable-select-row.vue';
import { languageMap } from 'boot/i18n';

const showSettingDialog = defineModel('showSettingDialog', { required: true, type: Boolean });
const userConfigStore = useUserConfigStore();

const userConfig = reactive(userConfigStore.getUserConfig.userConfig);

const { t, locale } = useI18n({ useScope: 'global' });

const layoutSettingOptions = [
  {
    value: 'sm',
    label: t('layoutSm')
  },
  {
    value: 'md',
    label: t('layoutMd')
  },
  {
    value: 'lg',
    label: t('layoutLg')
  }
];
const langSettingOptions = useI18n().availableLocales.map((locale) => ({
  value: locale,
  label: languageMap[locale]
}));

watch(userConfig, () => {
  userConfigStore.setUserConfig({
    ...userConfigStore.getUserConfig,
    userConfig: userConfig
  });
  userConfigStore.updateUserConfigToLocalStorage();
}, { deep: true });
</script>
