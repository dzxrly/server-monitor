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
      class="q-mt-sm"
      v-model:switch-value="userConfig.useFahrenheitUnit"
      :title="t('useFahrenheitUnit')"
    />
    <SelectRow
      class="q-mt-sm"
      v-model:select-value="userConfig.indexPageServerPanelLayout"
      :title="t('indexPageServerPanelLayout')"
      :options="layoutSettingOptions"
    />
    <SelectRow
      class="q-mt-sm"
      v-model:select-value="userConfig.defaultLanguage"
      :title="t('language')"
      :options="langSettingOptions"
      v-on:update:select-value="(val) => locale = val"
    />
    <NumberInputRow
      class="q-mt-sm"
      :title="t('refreshTimeSec')"
      v-model:value="userConfig.refreshTimeSec"
      :max="3600"
      :min="1"
      :step="1"
    />
    <NumberInputRow
      class="q-mt-sm"
      :title="t('freeUsageThreshold')"
      v-model:value="userConfig.freeUsageThreshold"
      :max="100"
      :min="0"
      :step="1"
    />
    <NumberInputRow
      class="q-mt-sm"
      :title="t('midUsageThreshold')"
      v-model:value="userConfig.midUsageThreshold"
      :max="100"
      :min="0"
      :step="1"
    />
    <div class="justify-center items-center full-width no-wrap q-mt-sm"
         :class="isLtSm ? 'column' : 'row' ">
      <div class="col-4 q-px-sm">
        <q-btn
          class="full-width"
          :label="t('resetSettingBtn')"
          color="negative"
          icon="restart_alt"
          @click="showResetConfirmDialog = true"
          outline
          rounded
          no-caps
        />
      </div>
      <div class="col-4 q-px-sm">
        <q-btn
          class="full-width"
          :label="t('resetSettingBtn')"
          color="negative"
          icon="restart_alt"
          outline
          rounded
          no-caps
        />
      </div>
      <div class="col-4 q-px-sm">
        <q-btn
          class="full-width"
          :label="t('resetSettingBtn')"
          color="negative"
          icon="restart_alt"
          outline
          rounded
          no-caps
        />
      </div>
    </div>

    <q-dialog
      v-model="showResetConfirmDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <div class="bg-transparent full-width text-base-color">
        <div class="column no-wrap justify-center items-center bg-card-color full-width q-pa-md rounded-borders">
          <div class="row justify-start items-center full-width">
            <span class="text-h6 text-base-color">{{ t('resetSettingConfirmTitle') }}</span>
          </div>
          <span class="text-body1 text-base-color q-mt-md">{{ t('resetSettingConfirm') }}</span>
          <div class="row justify-between items-center full-width q-mt-md">
            <q-btn
              class="col-5"
              :label="t('confirmBtn')"
              color="negative"
              @click="() => {
                resetSettings();
                showResetConfirmDialog = false;
              }"
              outline
              rounded
              no-caps
            />
            <q-btn
              class="col-5"
              :label="t('cancelBtn')"
              color="primary"
              @click="showResetConfirmDialog = false"
              outline
              rounded
              no-caps
            />
          </div>
        </div>
      </div>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ClickableSwitchRow from 'components/base/clickable-switch-row.vue';
import { useConfigStore } from 'stores/user-config';
import { computed, inject, ref, watch } from 'vue';
import { languageMap } from 'boot/i18n';
import SelectRow from 'components/base/select-row.vue';
import NumberInputRow from 'components/base/number-input-row.vue';
import { useQuasar } from 'quasar';

const showSettingDialog = defineModel('showSettingDialog', { required: true, type: Boolean });
const configStore = useConfigStore();

const userConfig = ref(configStore.config.userConfig);
const showResetConfirmDialog = ref(false);

const { t, locale } = useI18n({ useScope: 'global' });
const $q = useQuasar();

const layoutSettingOptions = computed(() => {
  return [
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
});
const langSettingOptions = useI18n().availableLocales.map((locale) => ({
  value: locale,
  label: languageMap[locale]
}));
const isLtSm = inject('isLtSm');

function resetSettings() {
  configStore.resetConfig();
  $q.notify({
    message: t('resetSettingSuccess'),
    color: 'positive',
    position: 'top'
  });
  locale.value = configStore.config.userConfig.defaultLanguage;
}

watch(userConfig, () => {
  configStore.setConfig({ ...configStore.config, userConfig: userConfig.value });
}, { deep: true });
</script>
