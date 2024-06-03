<template>
  <div class="bg-transparent full-width">
    <div class="column no-wrap justify-center items-center bg-info full-width q-pa-md rounded-borders">
      <div class="row justify-start items-center full-width">
        <span class="text-h6">{{ t('addServer') }}</span>
      </div>
      <div class="col-grow full-width q-pt-md">
        <div class="add-server-dialog-wrapper column no-wrap justify-center items-center full-width">
          <q-input
            class="full-width"
            v-model="serverConfig.uniqueId"
            :label="t('serverUUID')"
            outlined
            readonly
          />
          <q-input
            class="full-width q-mt-md"
            v-model="serverConfig.customName"
            :label="t('customServerName')"
            outlined
            clearable
          />
          <q-input
            class="full-width q-mt-md"
            v-model="serverConfig.serverUrl"
            :label="t('serverUrl')"
            outlined
            clearable
          />
          <q-input
            ref="tagColorInputRef"
            class="full-width q-mt-md"
            v-model="serverConfig.tagColor"
            :label="t('serverTagColor')"
            :rules="['hexColor']"
            outlined
            clearable
          >
            <template v-slot:prepend>
              <q-icon
                name="dns"
                size="lg"
                :style="{ color: serverConfig.tagColor }"
              />
            </template>
            <template v-slot:append>
              <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-color v-model="serverConfig.tagColor" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
      </div>
      <div class="row justify-evenly items-center full-width no-wrap q-pt-md">
        <q-btn
          no-caps
          outline
          class="col-5"
          color="negative"
          icon="close"
          :label="t('cancelBtn')"
          @click="showAddServerDialog = false" />
        <q-btn
          no-caps
          outline
          class="col-5"
          color="primary"
          icon="check"
          :label="t('confirmBtn')"
          :disable="!isValid"
          @click="addServer" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { ServerConfig } from 'src/module/user-config';
import { useI18n } from 'vue-i18n';
import { getUUID } from 'src/utils/utils';
import { useUserConfigStore } from 'stores/user-config';

const showAddServerDialog = defineModel('showAddServerDialog', { required: true, type: Boolean });
const serverConfig = reactive(new ServerConfig());
const { t } = useI18n();
const userConfigStore = useUserConfigStore();
const tagColorInputRef = ref();

const isValid = computed(() => {
  return serverConfig.serverUrl && serverConfig.serverUrl !== '' &&
    serverConfig.tagColor && serverConfig.tagColor !== '' &&
    serverConfig.uniqueId && serverConfig.uniqueId !== '' &&
    serverConfig.customName && serverConfig.customName !== '' &&
    !tagColorInputRef.value.hasError;
});

function addServer() {
  const serverList = userConfigStore.getUserConfig.userConfig.serverListConfig;
  serverList.push(serverConfig);
  userConfigStore.setUserConfig({
    ...userConfigStore.getUserConfig,
    userConfig: {
      ...userConfigStore.getUserConfig.userConfig,
      serverListConfig: serverList
    }
  });
  userConfigStore.updateUserConfigToLocalStorage();

  showAddServerDialog.value = false;
}

onMounted(() => {
  serverConfig.uniqueId = getUUID();
});
</script>
