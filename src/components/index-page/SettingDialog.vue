<template>
  <div
    class="setting-dialog-wrapper column justify-center items-center no-wrap full-width bg-card-color rounded-borders q-pa-md">
    <div class="row justify-between items-center full-width">
      <span class="text-card-color text-h6">{{ t('settings') }}</span>
      <q-btn
        icon="close"
        class="text-btn-color"
        color="btn-color"
        @click="showSettingDialog = false"
        round
        flat
      />
    </div>
    <ClickableSwitchRow
      class="q-mt-md"
      v-model:switch-value="config.darkMode"
      :title="t('darkMode')"
    />
    <ClickableSwitchRow
      class="q-mt-sm"
      v-model:switch-value="config.useFahrenheitUnit"
      :title="t('useFahrenheitUnit')"
    />
    <SelectRow
      class="q-mt-sm"
      v-model:select-value="config.indexPageServerPanelLayout"
      :title="t('indexPageServerPanelLayout')"
      :options="layoutSettingOptions"
    />
    <SelectRow
      class="q-mt-sm"
      v-model:select-value="config.defaultLanguage"
      :title="t('language')"
      :options="langSettingOptions"
      v-on:update:select-value="(val) => locale = val"
    />
    <NumberInputRow
      class="q-mt-sm"
      :title="t('refreshTimeSec')"
      v-model:value="config.refreshTimeSec"
      :max="3600"
      :min="1"
      :step="1"
    />
    <NumberInputRow
      class="q-mt-sm"
      :title="t('freeUsageThreshold')"
      v-model:value="config.freeUsageThreshold"
      :max="100"
      :min="0"
      :step="1"
    />
    <NumberInputRow
      class="q-mt-sm"
      :title="t('midUsageThreshold')"
      v-model:value="config.midUsageThreshold"
      :max="100"
      :min="0"
      :step="1"
    />
    <div class="row justify-evenly items-center full-width no-wrap q-mt-md">
      <q-btn
        :label="t('resetSettingBtn')"
        color="negative"
        @click="showResetConfirmDialog = true"
        flat
        rounded
        no-caps
      />
      <q-btn
        :label="t('exportSettingBtn')"
        color="btn-color"
        @click="configToJsonFile()"
        flat
        rounded
        no-caps
      />
      <q-btn
        :label="t('importSettingBtn')"
        color="btn-color"
        @click="importConfigFromJsonFile()"
        flat
        rounded
        no-caps
      />
    </div>

    <q-dialog
      v-model="showResetConfirmDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <div class="bg-transparent text-card-color">
        <div class="column no-wrap justify-center items-center bg-card-color full-width q-pa-md rounded-borders">
          <div class="row justify-start items-center full-width">
            <span class="text-h6 text-card-color">{{ t('resetSettingConfirmTitle') }}</span>
          </div>
          <span class="text-body1 text-card-color q-mt-md">{{ t('resetSettingConfirm') }}</span>
          <div class="row justify-evenly items-center full-width q-mt-md">
            <q-btn
              :label="t('confirmBtn')"
              color="negative"
              @click="() => {
                resetSettings();
                showResetConfirmDialog = false;
              }"
              flat
              rounded
              no-caps
            />
            <q-btn
              :label="t('cancelBtn')"
              color="btn-color"
              @click="showResetConfirmDialog = false"
              flat
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
import ClickableSwitchRow from 'components/base/ClickableSwitchRow.vue';
import { useConfigStore } from 'stores/user-config';
import { computed, ref, watch } from 'vue';
import { languageMap } from 'boot/i18n';
import SelectRow from 'components/base/SelectRow.vue';
import NumberInputRow from 'components/base/NumberInputRow.vue';
import { useQuasar } from 'quasar';
import { Config, configZod } from 'src/module/config';

const showSettingDialog = defineModel('showSettingDialog', { required: true, type: Boolean });
const configStore = useConfigStore();

const config = ref(configStore.config);
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

function resetSettings() {
  configStore.resetConfig();
  $q.notify({
    message: t('resetSettingSuccess'),
    color: 'positive',
    position: 'top'
  });
  locale.value = configStore.config.defaultLanguage;
}

function configToJsonFile() {
  const data = JSON.stringify(configStore.config, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'config.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importConfigFromJsonFile() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      const file = target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result;
        if (typeof result === 'string') {
          try {
            const zodParse = configZod.strict().partial().safeParse(JSON.parse(result));
            if (zodParse.success) {
              config.value = zodParse.data as Config;
              configStore.setConfig({
                ...configStore.config,
                ...zodParse.data as Config
              });
            } else {
              $q.notify({
                message: t('importSettingFailNotAConfigFile'),
                color: 'negative',
                position: 'top'
              });
            }
          } catch (e) {
            $q.notify({
              message: t('importSettingFailNotAConfigFile'),
              color: 'negative',
              position: 'top'
            });
          }
        }
      };
      reader.readAsText(file);
    } else {
      $q.notify({
        message: t('importSettingFailNoFile'),
        color: 'negative',
        position: 'top'
      });
    }
  };
  input.click();
}

watch(config, () => {
  configStore.setConfig({
    ...configStore.config,
    ...config.value
  });
}, { deep: true });
</script>
