<script setup lang="ts">
import { computed, onMounted, provide, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';

import { POLLING_PAUSED_KEY } from '@/features/monitoring/composables/polling-context';
import ServerFormDialog from '@/features/servers/components/ServerFormDialog.vue';
import SettingsDialog from '@/features/settings/components/SettingsDialog.vue';
import { useConfigStore } from '@/features/settings/stores/config-store';

const route = useRoute();
const router = useRouter();
const { t } = useI18n();
const configStore = useConfigStore();
const paused = ref(false);
const showSettings = ref(false);
const showEdit = ref(false);
const showDelete = ref(false);
const showBackendTip = ref(false);
const hideBackendTip = ref(false);
const currentServerId = computed(() => String(route.params.uid ?? ''));
const onDetailPage = computed(() => route.name === 'ServerDetail');

provide(POLLING_PAUSED_KEY, paused);

function deleteCurrentServer(): void {
  configStore.deleteServer(currentServerId.value);
  showDelete.value = false;
  void router.push({ name: 'Dashboard' });
}

function closeBackendTip(): void {
  showBackendTip.value = false;
  if (hideBackendTip.value) configStore.config.showBackendTipsDialog = false;
}

onMounted(() => {
  showBackendTip.value = configStore.config.showBackendTipsDialog;
});
</script>

<template>
  <q-layout view="hHh lpR fff" class="bg-default-color text-default-color">
    <q-page-container>
      <router-view />
      <q-page-sticky
        position="bottom-right"
        :offset="[14, 58]"
        class="floating-actions"
      >
        <div class="column q-gutter-sm">
          <q-btn
            round
            class="shadow-3 text-btn-color"
            color="btn-color"
            :icon="paused ? 'play_arrow' : 'pause'"
            :aria-label="paused ? t('resume') : t('pause')"
            @click="paused = !paused"
          />
          <q-btn
            v-if="!onDetailPage"
            round
            class="shadow-3 text-btn-color"
            color="btn-color"
            icon="settings"
            :aria-label="t('settings')"
            @click="showSettings = true"
          />
          <template v-else>
            <q-btn
              round
              class="shadow-3 text-btn-color"
              color="btn-color"
              icon="edit"
              :aria-label="t('serverSettings')"
              @click="showEdit = true"
            />
            <q-btn
              round
              class="shadow-3"
              color="negative"
              icon="delete_forever"
              :aria-label="t('deleteThisServer')"
              @click="showDelete = true"
            />
          </template>
        </div>
      </q-page-sticky>
    </q-page-container>

    <q-footer class="bg-transparent text-secondary q-py-sm">
      <div class="row justify-center items-center q-gutter-sm">
        <q-btn
          flat
          dense
          rounded
          no-caps
          size="sm"
          href="https://github.com/dzxrly/server-monitor/blob/main/LICENSE"
          target="_blank"
          label="APL-2.0"
        />
        <q-btn
          flat
          dense
          rounded
          no-caps
          size="sm"
          href="https://github.com/dzxrly/server-monitor"
          target="_blank"
          :label="t('sourceCode')"
        />
        <q-btn
          flat
          dense
          rounded
          no-caps
          size="sm"
          href="https://eggtargaryen.com"
          target="_blank"
          label="by Egg Targaryen"
        />
      </div>
    </q-footer>

    <q-dialog v-model="showSettings" persistent backdrop-filter="blur(5px)">
      <SettingsDialog v-model="showSettings" />
    </q-dialog>
    <q-dialog v-model="showEdit" persistent backdrop-filter="blur(5px)">
      <ServerFormDialog
        v-model="showEdit"
        mode="edit"
        :server-id="currentServerId"
      />
    </q-dialog>
    <q-dialog v-model="showDelete" backdrop-filter="blur(5px)">
      <q-card class="bg-card-color text-card-color rounded-borders">
        <q-card-section
          ><div class="text-h6">{{ t('deleteThisServer') }}</div>
          <p>{{ t('deleteThisServerConfirm') }}</p></q-card-section
        >
        <q-card-actions align="right"
          ><q-btn v-close-popup flat :label="t('cancelBtn')" /><q-btn
            flat
            color="negative"
            :label="t('confirmBtn')"
            @click="deleteCurrentServer"
        /></q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="showBackendTip" persistent backdrop-filter="blur(5px)">
      <q-card class="backend-tip bg-card-color text-card-color rounded-borders">
        <q-card-section>
          <div class="text-h6">{{ t('backendDeployTitle') }}</div>
          <p class="q-mt-md">
            {{ t('backendDeployDesc') }}
            <a
              href="https://github.com/dzxrly/server-monitor/tree/backend-dev"
              target="_blank"
              >{{ t('backendDeployDocs') }}</a
            >
          </p>
          <q-checkbox v-model="hideBackendTip" :label="t('noPopupTips')" />
        </q-card-section>
        <q-card-actions align="right"
          ><q-btn
            flat
            color="primary"
            :label="t('confirmBtn')"
            @click="closeBackendTip"
        /></q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<style scoped lang="scss">
.floating-actions {
  z-index: 10;
}

.floating-actions :deep(.q-btn) {
  opacity: 0.88;
  transition: opacity 0.2s ease;
}

.floating-actions :deep(.q-btn:hover),
.floating-actions :deep(.q-btn:focus-visible) {
  opacity: 1;
}

.backend-tip {
  width: min(92vw, 32rem);
  border: 1px solid var(--border-color);

  a {
    color: currentColor;
  }
}
</style>
