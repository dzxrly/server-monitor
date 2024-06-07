<template>
  <div
    class="server-edit-dialog-wrapper column justify-center items-center no-wrap full-width bg-card-color rounded-borders q-pa-md">
    <div class="row justify-between items-center full-width">
      <span class="text-card-color text-h6">{{ t('serverSettings') }}</span>
      <q-btn
        icon="close"
        class="text-btn-color"
        color="btn-color"
        @click="showDialog = false"
        round
        flat
      />
    </div>
    <div class="col-grow full-width q-pt-md column no-wrap justify-center items-center">
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
          outlined />
        <q-input
          ref="serverUrlInputRef"
          class="col-grow q-ml-xs"
          v-model="serverUrlInput"
          :label="t('serverUrl')"
          :hint="t('serverUrlInputFieldHint')"
          :rules="[ val => val && val.length > 0 || t('serverUrlInputFieldHintErrorMsg') ]"
          @change="() => serverConfig.serverUrl = `${serverUrlPrependUrlSelect}${serverUrlInput}`"
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
        :rules="[ val => val && val.length <= 10 || t('customServerNameInputFieldHintErrorMsg') ]"
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
            :style="{ color: tagColorInputError ? '#C10015' : serverConfig.tagColor }"
          />
        </template>
        <template v-slot:append>
          <q-icon name="colorize" class="cursor-pointer">
            <q-popup-proxy cover transition-show="scale" transition-hide="scale">
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
        outlined />
      <q-btn
        no-caps
        flat
        class="full-width rounded-borders q-mt-md"
        color="btn-color"
        icon="add"
        :label="t('saveEditBtn')"
        :disable="!isValid"
        @click="saveEdit" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { useConfigStore } from 'stores/user-config';
import { computed, reactive, ref } from 'vue';
import { GPUType, ServerConfig } from 'src/module/config';
import { useQuasar } from 'quasar';

const showDialog = defineModel('showDialog', { required: true, type: Boolean });

const props = defineProps({
  serverUniqueId: { required: true, type: String }
});

const { t } = useI18n();
const $q = useQuasar();
const configStore = useConfigStore();

const serverConfig = reactive<ServerConfig>(configStore.config.serverListConfig.find((server) => server.uniqueId === props.serverUniqueId) as ServerConfig);
const serverNameInputRef = ref();
const serverUrlInputRef = ref();
const tagColorInputRef = ref();
const tagColorInputError = computed(() => tagColorInputRef.value && tagColorInputRef.value.hasError);
const serverUrlPrependUrlSelect = ref(serverConfig.serverUrl.split('://')[0] + '://');
const serverUrlInput = ref(serverConfig.serverUrl.split('://')[1]);
const gpuTypeSelect = ref(serverConfig.gpuServer.gpuType);

const serverUrlPrependSelectOptions = [
  {
    label: 'https://',
    value: 'https://'
  },
  {
    label: 'http://',
    value: 'http://'
  }
];
// convert GPUType enum to map, like { label: 'NVIDIA', value: GPUType.NVIDIA }
const gpuTypeSelectOptions = (Object.keys(GPUType) as (keyof typeof GPUType)[]).map(key => {
  return {
    label: t(key),
    value: GPUType[key],
    // TODO: Only support NVIDIA GPU
    disable: GPUType[key] !== GPUType.NoneGPU && GPUType[key] !== GPUType.NVIDIA
  };
});

const isValid = computed(() => {
  return serverConfig.tagColor && serverConfig.tagColor !== '' &&
    serverConfig.uniqueId && serverConfig.uniqueId !== '' &&
    serverConfig.serverUrl && serverConfig.serverUrl !== '' &&
    serverConfig.customName && serverConfig.customName !== '' &&
    tagColorInputRef.value && !tagColorInputRef.value.hasError &&
    serverNameInputRef.value && !serverNameInputRef.value.hasError &&
    serverUrlInputRef.value && !serverUrlInputRef.value.hasError;
});

function saveEdit() {
  if (isValid.value) {
    const serverList = configStore.config.serverListConfig;
    const index = serverList.findIndex((server) => server.uniqueId === props.serverUniqueId);
    serverList[index] = serverConfig;
    configStore.setConfig({
      ...configStore.config,
      serverListConfig: serverList
    });
    showDialog.value = false;
  } else $q.notify({
    type: 'negative',
    message: t('serverEditDialogSaveErrorMsg'),
    icon: 'warning'
  });
}
</script>
