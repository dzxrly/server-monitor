<template>
  <q-page class="index-page-wrapper" :class="{ 'q-ma-xs': isLtSm }">
    <div class="full-width row wrap justify-start items-stretch">
      <ServerCard
        class="col-xs-12 col-sm-12 col-md-4 col-lg-3 col-xl-3"
        v-for="server in serverList"
        :key="server.uniqueId"
        :server-config="server"
        :show-layout="userConfig.indexPageServerPanelLayout"
        :use-fahrenheit-unit="userConfig.darkMode"
        :refresh-time-sec="userConfig.refreshTimeSec"
        :free-usage-threshold="userConfig.freeUsageThreshold"
        :mid-usage-threshold="userConfig.midUsageThreshold"
      />
      <div class="add-server-card-wrapper col-xs-12 col-sm-12 col-md-4 col-lg-3 col-xl-3 q-pa-sm bg-transparent">
        <div
          class="add-server-card rounded-borders column no-wrap justify-center items-center cursor-pointer bg-card-color q-px-md q-py-xl full-height"
          @click="showAddServerDialog = true"
        >
          <q-icon class="q-mb-md" color="text-base-color" name="add" size="xl" />
          <span class="text-subtitle1 text-base-color">{{ t('addServer') }}</span>
        </div>
      </div>
    </div>

    <q-dialog
      v-model="showAddServerDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <AddServerDialog v-model:show-add-server-dialog="showAddServerDialog" />
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { useUserConfigStore } from 'stores/user-config';
import { inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import AddServerDialog from 'components/index-page/add-server-dialog.vue';
import { ServerConfig } from 'src/module/user-config';
import ServerCard from 'components/index-page/server-card.vue';

const userConfigStore = useUserConfigStore();
const { t } = useI18n();

const serverList = ref<Array<ServerConfig>>(userConfigStore.getUserConfig.userConfig.serverListConfig);
const userConfig = ref(userConfigStore.getUserConfig.userConfig);
const showAddServerDialog = ref(false);
const isLtSm = inject('isLtSm');
</script>

<style lang="sass" scoped>
.index-page-wrapper
  transition: all 0.2s ease-in-out

  .add-server-card-wrapper
    transition: all 0.2s ease-in-out

    .add-server-card
      box-shadow: none
      transition: all 0.2s ease-in-out

    .add-server-card:hover
      box-shadow: 0 2px 4px -1px #0003, 0 4px 5px #00000024, 0 1px 10px #0000001f
</style>
