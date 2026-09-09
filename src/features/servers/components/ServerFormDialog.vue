<script setup lang="ts">
import { Notify } from 'quasar';
import { computed, nextTick, reactive, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import {
  type ServerConfig,
  createServerId,
} from '@/features/settings/model/config';
import { useConfigStore } from '@/features/settings/stores/config-store';

const visible = defineModel<boolean>({ required: true });
const props = withDefaults(
  defineProps<{
    mode?: 'add' | 'edit';
    serverId?: string;
  }>(),
  { mode: 'add', serverId: '' },
);

const { t } = useI18n();
const configStore = useConfigStore();
const formRef = ref<{
  validate: () => Promise<boolean>;
  resetValidation: () => void;
}>();
const server = reactive<ServerConfig>(emptyServer());
const saving = ref(false);
const saveError = ref('');
const existingServer = computed(() =>
  configStore.config.serverListConfig.find(
    (candidate) => candidate.uniqueId === props.serverId,
  ),
);
const missingServer = computed(
  () => props.mode === 'edit' && !existingServer.value,
);
const title = computed(() =>
  props.mode === 'add' ? t('addServer') : t('serverSettings'),
);
const gpuType = computed({
  get: () => server.gpuServer?.gpuType ?? 'NoneGPU',
  set: (value: string) => {
    server.gpuServer = { gpuType: value };
  },
});
const gpuTypeOptions = computed(() => [
  { label: t('NoneGPU'), value: 'NoneGPU' },
  { label: t('NVIDIA'), value: 'NVIDIA' },
  { label: t('AMD'), value: 'AMD', disable: true },
  { label: t('INTEL'), value: 'Intel', disable: true },
]);

function randomColor(): string {
  return `#${Math.floor(Math.random() * 0x1000000)
    .toString(16)
    .padStart(6, '0')}`;
}

function emptyServer(): ServerConfig {
  return {
    customName: '',
    uniqueId: createServerId(),
    serverUrl: 'http://127.0.0.1:6543',
    tagColor: randomColor(),
    gpuServer: { gpuType: 'NoneGPU' },
  };
}

function copyServer(value: ServerConfig): ServerConfig {
  return {
    customName: value.customName,
    uniqueId: value.uniqueId,
    serverUrl: value.serverUrl,
    tagColor: value.tagColor,
    gpuServer: { gpuType: value.gpuServer?.gpuType ?? 'NoneGPU' },
  };
}

function load(): void {
  saveError.value = '';
  if (props.mode === 'add') Object.assign(server, emptyServer());
  else if (existingServer.value)
    Object.assign(server, copyServer(existingServer.value));
  void nextTick(() => formRef.value?.resetValidation());
}

async function save(): Promise<void> {
  if (saving.value || missingServer.value) return;
  const mode = props.mode;
  const serverId = props.serverId;
  saving.value = true;
  saveError.value = '';
  try {
    if (!(await formRef.value?.validate())) return;
    if (!visible.value || props.mode !== mode || props.serverId !== serverId)
      return;

    const updated = copyServer(server);
    updated.serverUrl = updated.serverUrl.replace(/\/+$/, '');
    if (mode === 'edit') {
      if (!configStore.updateServer(serverId, updated)) {
        saveError.value = t('serverNotFound');
        return;
      }
    } else configStore.addServer(updated);
    Notify.create({
      message: t('settingsSaved'),
      color: 'primary',
      icon: 'check',
      timeout: 1000,
    });
    visible.value = false;
  } finally {
    saving.value = false;
  }
}

watch(
  [visible, () => props.mode, () => props.serverId],
  ([isVisible]) => {
    if (isVisible) load();
  },
  { immediate: true },
);
</script>

<template>
  <q-card
    class="dialog-card bg-card-color text-card-color rounded-borders full-width"
  >
    <q-form ref="formRef" @submit.prevent="save">
      <q-card-section>
        <header class="row items-center no-wrap q-mb-md">
          <q-icon
            :name="mode === 'add' ? 'add' : 'edit'"
            size="sm"
            class="q-mr-sm"
          />
          <span class="text-h6 col">{{ title }}</span>
          <q-btn round flat icon="close" @click="visible = false" />
        </header>
        <q-banner
          v-if="missingServer || saveError"
          rounded
          class="bg-negative text-white q-mb-md"
          role="alert"
        >
          {{ missingServer ? t('serverNotFound') : saveError }}
        </q-banner>
        <template v-if="!missingServer">
          <q-input
            v-model="server.uniqueId"
            :label="t('serverUUID')"
            outlined
            readonly
          />
          <q-input
            v-model.trim="server.serverUrl"
            class="q-mt-md"
            :label="t('serverUrl')"
            :hint="t('apiV1UrlHint')"
            :rules="[
              (value) =>
                /^https?:\/\/.+/i.test(value) ||
                t('serverUrlInputFieldHintErrorMsg'),
            ]"
            outlined
            clearable
          />
          <q-input
            v-model.trim="server.customName"
            class="q-mt-sm"
            :label="t('customServerName')"
            :rules="[
              (value) =>
                (typeof value === 'string' &&
                  value.length >= 1 &&
                  value.length <= 64) ||
                t('customServerNameInputFieldHintErrorMsg'),
            ]"
            outlined
            clearable
          />
          <q-input
            v-model="server.tagColor"
            class="q-mt-sm"
            :label="t('serverTagColor')"
            :rules="[
              (value) =>
                /^#[0-9a-f]{6}$/i.test(value) ||
                t('serverTagColorHintErrorMsg'),
            ]"
            outlined
          >
            <template #prepend>
              <q-icon name="dns" :style="{ color: server.tagColor }" />
            </template>
            <template #append>
              <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy
                  cover
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-color v-model="server.tagColor" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-select
            v-model="gpuType"
            class="q-mt-md"
            :options="gpuTypeOptions"
            :label="t('serverGPUType')"
            map-options
            emit-value
            outlined
          />
        </template>
      </q-card-section>
      <q-card-actions align="right" class="q-px-md q-pb-md">
        <q-btn
          flat
          rounded
          no-caps
          :label="t('cancelBtn')"
          @click="visible = false"
        />
        <q-btn
          color="primary"
          rounded
          no-caps
          type="submit"
          icon="save"
          :loading="saving"
          :disable="missingServer"
          :label="mode === 'add' ? t('addBtn') : t('saveEditBtn')"
        />
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<style scoped>
.dialog-card {
  width: min(92vw, 34rem);
  border: 0;
}
</style>
