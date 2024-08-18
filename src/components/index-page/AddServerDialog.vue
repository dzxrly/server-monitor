<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { GPUType, ServerConfig } from 'src/module/config';
import { useI18n } from 'vue-i18n';
import { getUUID } from 'src/utils/utils';
import { useConfigStore } from 'stores/user-config';

const showAddServerDialog = defineModel('showAddServerDialog', {
  required: true,
  type: Boolean,
});
const serverConfig = reactive<ServerConfig>(new ServerConfig());
const { t } = useI18n();
const configStore = useConfigStore();
const serverNameInputRef = ref();
const serverUrlInputRef = ref();
const tagColorInputRef = ref();
const tagColorInputError = computed(
  () => tagColorInputRef.value && tagColorInputRef.value.hasError
);
const serverUrlPrependUrlSelect = ref('https://');
const serverUrlInput = ref('');
const gpuTypeSelect = ref(GPUType.NoneGPU);

const serverUrlPrependSelectOptions = [
  {
    label: 'https://',
    value: 'https://',
  },
  {
    label: 'http://',
    value: 'http://',
  },
];
// convert GPUType enum to map, like { label: 'NVIDIA', value: GPUType.NVIDIA }
const gpuTypeSelectOptions = (
  Object.keys(GPUType) as (keyof typeof GPUType)[]
).map((key) => {
  return {
    label: t(key),
    value: GPUType[key],
    // TODO: Only support NVIDIA GPU
    disable:
      GPUType[key] !== GPUType.NoneGPU && GPUType[key] !== GPUType.NVIDIA,
  };
});

const isValid = computed(() => {
  return (
    serverConfig.tagColor &&
    serverConfig.tagColor !== '' &&
    serverConfig.uniqueId &&
    serverConfig.uniqueId !== '' &&
    serverConfig.serverUrl &&
    serverConfig.serverUrl !== '' &&
    serverConfig.customName &&
    serverConfig.customName !== '' &&
    tagColorInputRef.value &&
    !tagColorInputRef.value.hasError &&
    serverNameInputRef.value &&
    !serverNameInputRef.value.hasError &&
    serverUrlInputRef.value &&
    !serverUrlInputRef.value.hasError
  );
});

function addServer() {
  const serverList = configStore.config.serverListConfig;
  serverList.push(serverConfig);
  configStore.setConfig({
    ...configStore.config,
    serverListConfig: serverList,
  });
  showAddServerDialog.value = false;
}

function generateRandomColor(): string {
  const randomHex = () =>
    Math.floor(Math.random() * 0x1000000)
      .toString(16)
      .padStart(6, '0');
  return `#${randomHex()}`;
}

onMounted(() => {
  serverConfig.uniqueId = getUUID();
  serverConfig.tagColor = generateRandomColor();
});

watch(serverUrlPrependUrlSelect, (newVal) => {
  serverConfig.serverUrl = `${newVal}${serverUrlInput.value}`;
});

watch(gpuTypeSelect, (newVal) => {
  serverConfig.gpuServer.setGPUType(newVal);
});
</script>

<template>
  <div
    class="add-server-dialog-wrapper full-width bg-transparent text-card-color"
  >
    <div
      class="column no-wrap justify-center items-center bg-card-color full-width q-pa-md rounded-borders"
    >
      <div class="row justify-between items-center full-width">
        <div class="row justify-start items-center">
          <q-icon class="text-card-color q-pr-sm" name="add" size="sm" />
          <span class="text-h6 text-card-color">{{ t('addServer') }}</span>
        </div>
        <q-btn
          color="btn-color"
          icon="close"
          @click="showAddServerDialog = false"
          flat
          round
        />
      </div>
      <div
        class="col-grow full-width q-pt-md column no-wrap justify-center items-center"
      >
        <q-input
          class="full-width"
          v-model="serverConfig.uniqueId"
          :label="t('serverUUID')"
          outlined
          readonly
        />
        <div class="full-width q-mt-md row justify-center items-start">
          <q-select
            v-model="serverUrlPrependUrlSelect"
            :options="serverUrlPrependSelectOptions"
            map-options
            emit-value
            outlined
          />
          <q-input
            ref="serverUrlInputRef"
            class="col-grow q-ml-xs"
            v-model="serverUrlInput"
            :label="t('serverUrl')"
            :hint="t('serverUrlInputFieldHint')"
            :rules="[
              (val) =>
                (val && val.length > 0) || t('serverUrlInputFieldHintErrorMsg'),
            ]"
            @change="
              () =>
                (serverConfig.serverUrl = `${serverUrlPrependUrlSelect}${serverUrlInput}`)
            "
            outlined
            clearable
          />
        </div>
        <q-input
          ref="serverNameInputRef"
          class="full-width q-mt-md"
          v-model="serverConfig.customName"
          :label="t('customServerName')"
          :hint="t('customServerNameInputFieldHint')"
          :rules="[
            (val) =>
              (val && val.length <= 16) ||
              t('customServerNameInputFieldHintErrorMsg'),
          ]"
          outlined
          clearable
        />
        <q-input
          ref="tagColorInputRef"
          class="full-width q-mt-md"
          v-model="serverConfig.tagColor"
          :label="t('serverTagColor')"
          :hint="t('serverTagColorHint')"
          :rules="['hexColor']"
          outlined
          clearable
        >
          <template v-slot:prepend>
            <q-icon
              :name="tagColorInputError ? 'warning' : 'dns'"
              size="md"
              :style="{
                color: tagColorInputError ? '#C10015' : serverConfig.tagColor,
              }"
            />
          </template>
          <template v-slot:append>
            <q-icon name="colorize" class="cursor-pointer">
              <q-popup-proxy
                cover
                transition-show="scale"
                transition-hide="scale"
              >
                <q-color v-model="serverConfig.tagColor" />
              </q-popup-proxy>
            </q-icon>
          </template>
          <template v-slot:error>
            {{ t('serverTagColorHintErrorMsg') }}
          </template>
        </q-input>
        <q-select
          class="full-width q-mt-md"
          v-model="gpuTypeSelect"
          :options="gpuTypeSelectOptions"
          :label="t('serverGPUType')"
          map-options
          emit-value
          outlined
        />
      </div>
      <q-btn
        no-caps
        flat
        class="full-width rounded-borders q-mt-md"
        color="btn-color"
        icon="add"
        :label="t('addBtn')"
        :disable="!isValid"
        @click="addServer"
      />
    </div>
  </div>
</template>

<style lang="sass" scoped>
.add-server-dialog-wrapper
  transition: all 0.25s ease-in-out
</style>
