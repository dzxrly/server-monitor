<script setup lang="ts">
import SettingDialog from 'components/index-page/SettingDialog.vue';
import { onMounted, provide, ref } from 'vue';
import { openURL } from 'quasar';
import { useRoute, useRouter } from 'vue-router';
import { ServerConfig } from 'src/module/config';
import { useConfigStore } from 'stores/user-config';
import { useI18n } from 'vue-i18n';
import ServerEditDialog from 'components/server-detail-page/ServerEditDialog.vue';

const $route = useRoute();
const $router = useRouter();
const configStore = useConfigStore();
const { t } = useI18n();

const showSettingDialog = ref(false);
const pauseFetch = ref<boolean>(false);
const showDeleteServerDialog = ref(false);
const showServerEditDialog = ref(false);
const showBackendDeployDialog = ref(true);
const noMoreBackendDeployTips = ref(false);

function deleteServer() {
  const newServerList = configStore.config.serverListConfig.filter(
    (server: ServerConfig) => server.uniqueId !== ($route.params.uid as string)
  );
  configStore.setConfig({
    ...configStore.config,
    serverListConfig: newServerList,
  });
  showDeleteServerDialog.value = false;
  $router.push('/');
}

function closeBackendDeployDialog() {
  showBackendDeployDialog.value = false;
  if (noMoreBackendDeployTips.value) {
    configStore.setConfig({
      ...configStore.config,
      showBackendTipsDialog: false,
    });
  }
}

provide('pauseFetch', pauseFetch);

onMounted(() => {
  showBackendDeployDialog.value = configStore.config.showBackendTipsDialog;
});
</script>

<template>
  <q-layout view="hHh lpR fff">
    <q-page-container>
      <router-view />

      <q-page-sticky>
        <div class="q-pa-md column justify-center items-center no-wrap">
          <q-btn
            class="sticky-btn shadow-4 text-btn-color"
            color="btn-color"
            :icon="pauseFetch ? 'play_arrow' : 'pause'"
            size="md"
            @click="pauseFetch = !pauseFetch"
            round
          />
          <q-btn
            v-if="$route.name === 'IndexPage'"
            class="sticky-btn shadow-4 q-mt-md text-btn-color"
            color="btn-color"
            icon="settings"
            size="md"
            @click="showSettingDialog = true"
            round
          />
          <q-btn
            v-if="$route.name === 'ServerDetail'"
            class="sticky-btn shadow-4 q-mt-md text-btn-color"
            icon="edit"
            color="btn-color"
            size="md"
            @click="showServerEditDialog = true"
            round
          />
          <q-btn
            v-if="$route.name === 'ServerDetail'"
            class="sticky-btn shadow-4 q-mt-md"
            icon="delete_forever"
            color="negative"
            size="md"
            @click="showDeleteServerDialog = true"
            round
          />
        </div>
      </q-page-sticky>
    </q-page-container>

    <q-footer
      class="bg-transparent text-secondary column justify-center items-center q-py-sm"
    >
      <div class="row justify-center items-center full-width">
        <div class="row justify-center items-center q-mr-sm">
          <q-icon class="q-mr-xs" name="mdi-license" size="xs" />
          <span>APL-2.0</span>
        </div>
        <div
          class="link-row row justify-center items-center cursor-pointer"
          @click="openURL('https://github.com/dzxrly/server-monitor')"
        >
          <q-icon class="q-mr-xs" name="fa-brands fa-github" size="xs" />
          <span>{{ t('sourceCode') }}</span>
        </div>
      </div>
      <div class="row justify-center items-center full-width">
        <span
          class="link-row cursor-pointer"
          @click="
            openURL(
              'https://github.com/dzxrly/server-monitor/blob/main/Privacy.md'
            )
          "
          >{{ t('privacyPolicy') }}
        </span>
        <span>&nbsp;|&nbsp;by&nbsp;</span>
        <span
          class="link-row cursor-pointer"
          @click="openURL('https://dzxrly.github.io/')"
          >Egg Targaryen</span
        >
      </div>
    </q-footer>

    <q-dialog
      v-model="showSettingDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <SettingDialog v-model:show-setting-dialog="showSettingDialog" />
    </q-dialog>

    <q-dialog
      v-model="showDeleteServerDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <q-card class="bg-card-color rounded-borders full-width">
        <q-card-section class="column justify-center items-center no-wrap">
          <div class="row justify-start items-center no-wrap full-width">
            <span class="text-card-color text-h6">{{
              t('deleteThisServer')
            }}</span>
          </div>
          <div
            class="row justify-start items-center no-wrap full-width q-mt-md"
          >
            <span class="text-card-color text-body1">{{
              t('deleteThisServerConfirm')
            }}</span>
          </div>
          <div
            class="row justify-evenly items-center no-wrap full-width q-mt-md"
          >
            <q-btn
              :label="t('confirmBtn')"
              color="negative"
              size="md"
              @click="deleteServer"
              no-caps
              flat
              rounded
            />
            <q-btn
              :label="t('cancelBtn')"
              color="primary"
              size="md"
              @click="showDeleteServerDialog = false"
              no-caps
              flat
              rounded
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="showServerEditDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <ServerEditDialog
        v-model:show-dialog="showServerEditDialog"
        :server-unique-id="$route.params.uid as string"
      />
    </q-dialog>

    <q-dialog
      v-model="showBackendDeployDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <q-card class="bg-card-color rounded-borders full-width">
        <q-card-section class="column justify-center items-center no-wrap">
          <div class="row justify-start items-center no-wrap full-width">
            <span class="text-card-color text-h6">{{
              t('backendDeployTitle')
            }}</span>
          </div>
          <div
            class="row justify-start items-center no-wrap full-width q-mt-md"
          >
            <span class="text-card-color text-body1"
              >{{ t('backendDeployDesc') }}
              <span
                class="cursor-pointer"
                style="text-decoration: underline"
                @click="
                  openURL(
                    'https://github.com/dzxrly/server-monitor/blob/backend/README.md'
                  )
                "
              >
                {{ t('backendDeployDocs') }}
              </span>
            </span>
          </div>
          <div class="row justify-end items-center no-wrap full-width q-mt-md">
            <div class="row justify-center items-center no-wrap">
              <q-checkbox v-model="noMoreBackendDeployTips" />
              <span>{{ t('noPopupTips') }}</span>
            </div>
          </div>
          <div
            class="row justify-evenly items-center no-wrap full-width q-mt-md"
          >
            <q-btn
              :label="t('confirmBtn')"
              color="primary"
              size="md"
              @click="closeBackendDeployDialog"
              no-caps
              flat
              rounded
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<style lang="sass" scoped>
.sticky-btn
  opacity: 1
  animation-name: sticky-btn-hide
  animation-duration: 5s
  animation-iteration-count: 1
  animation-direction: normal
  animation-fill-mode: forwards

.sticky-btn:hover, .sticky-btn:focus
  animation-play-state: paused
  opacity: 1 !important

.link-row
  text-decoration: none

.link-row:hover
  text-decoration: underline

@keyframes sticky-btn-hide
  0%
    opacity: 1
  100%
    opacity: 0.2
</style>
