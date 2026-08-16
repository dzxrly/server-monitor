<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useQuasar } from 'quasar';

import { languageMap } from '@/boot/i18n';
import {
  type AppConfig,
  normalizeConfig,
  partialConfigSchema,
} from '@/features/settings/model/config';
import { useConfigStore } from '@/features/settings/stores/config-store';

const visible = defineModel<boolean>({ required: true });
const configStore = useConfigStore();
const $q = useQuasar();
const { t, locale, availableLocales } = useI18n({ useScope: 'global' });
const showResetConfirm = ref(false);
const config = computed(() => configStore.config);

const languageOptions = computed(() =>
  availableLocales.map((value) => ({
    value,
    label: languageMap[value] ?? value,
  })),
);
const layoutOptions = computed(() => [
  { value: 'sm', label: t('layoutSm') },
  { value: 'md', label: t('layoutMd') },
  { value: 'lg', label: t('layoutLg') },
]);
const unitOptions = ['B', 'KB', 'MB', 'GB', 'TB'].map((value) => ({
  value,
  label: value,
}));

function saveAndClose(): void {
  configStore.setConfig(
    normalizeConfig(JSON.parse(JSON.stringify(config.value)) as unknown),
  );
  locale.value = configStore.config.defaultLanguage;
  visible.value = false;
}

function reset(): void {
  configStore.resetConfig();
  locale.value = configStore.config.defaultLanguage;
  showResetConfirm.value = false;
}

function exportConfig(): void {
  const blob = new Blob([JSON.stringify(config.value, null, 2)], {
    type: 'application/json',
  });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = 'server-monitor-config.json';
  anchor.click();
  URL.revokeObjectURL(url);
}

function importConfig(): void {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/json,.json';
  input.addEventListener('change', () => {
    const file = input.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.addEventListener('load', () => {
      try {
        const raw = JSON.parse(String(reader.result));
        const parsed = partialConfigSchema.safeParse(raw);
        if (!parsed.success) throw new Error('invalid config');
        const servers = parsed.data.serverListConfig ?? [];
        const ids = servers.map((server) => server.uniqueId);
        if (new Set(ids).size !== ids.length) throw new Error('duplicate ids');
        configStore.setConfig(
          normalizeConfig({ ...config.value, ...parsed.data }),
        );
        locale.value = configStore.config.defaultLanguage;
      } catch {
        $q.notify({
          type: 'negative',
          message: t('importSettingFailNotAConfigFile'),
        });
      }
    });
    reader.readAsText(file);
  });
  input.click();
}

function updateLanguage(value: string): void {
  config.value.defaultLanguage = value as AppConfig['defaultLanguage'];
  locale.value = value;
}
</script>

<template>
  <q-card
    class="settings-card bg-card-color text-card-color rounded-borders full-width"
  >
    <q-card-section>
      <header class="row items-center no-wrap q-mb-md">
        <q-icon name="settings" size="sm" class="q-mr-sm" />
        <span class="text-h6 col">{{ t('settings') }}</span>
        <q-btn round flat icon="close" @click="visible = false" />
      </header>

      <q-list class="settings-list">
        <q-item tag="label" clickable>
          <q-item-section
            ><q-item-label>{{ t('darkMode') }}</q-item-label></q-item-section
          >
          <q-item-section side
            ><q-toggle v-model="config.darkMode" color="positive"
          /></q-item-section>
        </q-item>
        <q-item tag="label" clickable>
          <q-item-section
            ><q-item-label>{{
              t('useFahrenheitUnit')
            }}</q-item-label></q-item-section
          >
          <q-item-section side
            ><q-toggle v-model="config.useFahrenheitUnit" color="positive"
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{
              t('indexPageServerPanelLayout')
            }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-select
              v-model="config.indexPageServerPanelLayout"
              :options="layoutOptions"
              emit-value
              map-options
              dense
              outlined
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{ t('language') }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-select
              :model-value="config.defaultLanguage"
              :options="languageOptions"
              emit-value
              map-options
              dense
              outlined
              @update:model-value="updateLanguage"
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{
              t('refreshTimeSec')
            }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-input
              v-model.number="config.refreshTimeSec"
              type="number"
              min="1"
              max="3600"
              dense
              outlined
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{
              t('processLimit')
            }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-input
              v-model.number="config.processLimit"
              type="number"
              min="1"
              max="50"
              dense
              outlined
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{ t('memoryUnit') }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-select
              v-model="config.memoryUnit"
              :options="unitOptions"
              emit-value
              map-options
              dense
              outlined
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{
              t('gpuMemoryUnit')
            }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-select
              v-model="config.gpuMemoryUnit"
              :options="unitOptions"
              emit-value
              map-options
              dense
              outlined
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{
              t('freeUsageThreshold')
            }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-input
              v-model.number="config.freeUsageThreshold"
              type="number"
              min="0"
              max="100"
              dense
              outlined
          /></q-item-section>
        </q-item>
        <q-item>
          <q-item-section
            ><q-item-label>{{
              t('midUsageThreshold')
            }}</q-item-label></q-item-section
          >
          <q-item-section side class="setting-control"
            ><q-input
              v-model.number="config.midUsageThreshold"
              type="number"
              min="0"
              max="100"
              dense
              outlined
          /></q-item-section>
        </q-item>
      </q-list>
    </q-card-section>
    <q-card-actions class="settings-actions q-px-md q-pb-md" align="between">
      <q-btn
        flat
        rounded
        no-caps
        color="negative"
        icon="restart_alt"
        :label="t('resetSettingBtn')"
        @click="showResetConfirm = true"
      />
      <div class="settings-actions__group">
        <q-btn
          flat
          rounded
          no-caps
          icon="file_upload"
          :label="t('exportSettingBtn')"
          :aria-label="t('exportSettingBtn')"
          @click="exportConfig"
        />
        <q-btn
          flat
          rounded
          no-caps
          icon="file_download"
          :label="t('importSettingBtn')"
          :aria-label="t('importSettingBtn')"
          @click="importConfig"
        />
        <q-btn
          color="primary"
          rounded
          no-caps
          :label="t('confirmBtn')"
          @click="saveAndClose"
        />
      </div>
    </q-card-actions>
  </q-card>

  <q-dialog v-model="showResetConfirm">
    <q-card class="bg-card-color text-card-color rounded-borders">
      <q-card-section
        ><div class="text-h6">{{ t('resetSettingConfirmTitle') }}</div>
        <p>{{ t('resetSettingConfirm') }}</p></q-card-section
      >
      <q-card-actions align="right"
        ><q-btn v-close-popup flat :label="t('cancelBtn')" /><q-btn
          flat
          color="negative"
          :label="t('confirmBtn')"
          @click="reset"
      /></q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped lang="scss">
.settings-card {
  width: min(94vw, 38rem);
  max-height: 88vh;
  overflow: auto;
  border: 0;
}

.settings-list {
  display: grid;
  gap: 0.25rem;

  :deep(.q-item) {
    border-radius: 12px;
    background: var(--bg-section-color);
  }
}

.setting-control {
  width: 10rem;
}

.settings-actions {
  gap: 0.5rem;
}

.settings-actions__group {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.25rem;
  margin-left: auto;
}

@media (max-width: 520px) {
  .setting-control {
    width: 8rem;
  }

  .settings-actions__group {
    flex: 1 1 100%;
  }
}
</style>
