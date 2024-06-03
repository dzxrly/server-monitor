<template>
  <q-page class="index-page-wrapper q-pa-md">
    <span>{{ serverList }}</span>
    <div class="full-width row wrap justify-start items-start">
      <div
        class="add-server-card rounded-borders column no-wrap justify-center items-center cursor-pointer bg-info"
        :style="{ width: isLtSm ? '100%' : '200px', height: isLtSm ? '200px' : '300px' }"
        @click="showAddServerDialog = true"
      >
        <q-icon class="q-mb-md" name="add" size="xl" />
        <span class="text-subtitle1">{{ t('addServer') }}</span>
      </div>
    </div>

    <q-dialog
      v-model="showAddServerDialog"
      backdrop-filter="blur(5px)"
      transition-duration="250"
      persistent
      no-shake
    >
      <AddServerDialog v-model:show-add-server-dialog="showAddServerDialog"></AddServerDialog>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { useUserConfigStore } from 'stores/user-config';
import { inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import AddServerDialog from 'components/index-page/add-server-dialog.vue';
import { ServerConfig } from 'src/module/user-config';

const userConfigStore = useUserConfigStore();
const { t } = useI18n();

const serverList = ref<Array<ServerConfig>>(userConfigStore.getUserConfig.userConfig.serverListConfig);
const isLtSm = inject<boolean>('isLtSm');
const showAddServerDialog = ref(false);
</script>

<style lang="sass" scoped>
.index-page-wrapper

  .add-server-card
    box-shadow: none
    transition: all 0.2s ease-in-out

  .add-server-card:hover
    box-shadow: 0 5px 5px -3px #0003, 0 8px 10px 1px #00000024, 0 3px 14px 2px #0000001f
</style>
