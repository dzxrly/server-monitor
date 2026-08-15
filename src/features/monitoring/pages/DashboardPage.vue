<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

import ServerCard from '@/features/monitoring/components/dashboard/ServerCard.vue';
import ServerFormDialog from '@/features/servers/components/ServerFormDialog.vue';
import { useConfigStore } from '@/features/settings/stores/config-store';

const configStore = useConfigStore();
const { t } = useI18n();
const showAddServer = ref(false);
</script>

<template>
  <q-page class="dashboard-page q-pa-sm q-pa-md-md">
    <div
      class="server-grid"
      :class="`server-grid-${configStore.config.indexPageServerPanelLayout}`"
    >
      <ServerCard
        v-for="server in configStore.config.serverListConfig"
        :key="server.uniqueId"
        :server="server"
        :layout="configStore.config.indexPageServerPanelLayout"
        :refresh-seconds="configStore.config.refreshTimeSec"
        :process-limit="configStore.config.processLimit"
        :fahrenheit="configStore.config.useFahrenheitUnit"
        :free-threshold="configStore.config.freeUsageThreshold"
        :mid-threshold="configStore.config.midUsageThreshold"
      />
      <q-card
        flat
        class="add-server-card bg-card-color text-card-color rounded-borders cursor-pointer"
        role="button"
        tabindex="0"
        @click="showAddServer = true"
        @keydown.enter="showAddServer = true"
      >
        <q-card-section
          class="full-height column items-center justify-center q-pa-lg"
        >
          <q-icon name="add" size="lg" />
          <span class="text-subtitle1 q-mt-sm">{{ t('addServer') }}</span>
        </q-card-section>
      </q-card>
    </div>

    <q-dialog v-model="showAddServer" persistent backdrop-filter="blur(5px)">
      <ServerFormDialog v-model="showAddServer" mode="add" />
    </q-dialog>
  </q-page>
</template>

<style scoped lang="scss">
.dashboard-page {
  max-width: 1920px;
  margin: 0 auto;
}

.server-grid {
  display: grid;
  align-items: stretch;
  gap: 0.75rem;
}

.server-grid-sm {
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 16.5rem), 1fr));
}

.server-grid-md {
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 20rem), 1fr));
}

.server-grid-lg {
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 24rem), 1fr));
}

.add-server-card {
  min-height: 12rem;
  border: 0;
  background: var(--bg-section-color) !important;
  box-shadow: none;
  transition: background-color 0.2s ease;

  &:hover,
  &:focus-visible {
    background: var(--bg-section-strong-color) !important;
  }

  &:focus-visible {
    outline: 2px solid var(--text-muted-color);
    outline-offset: 2px;
  }
}
</style>
