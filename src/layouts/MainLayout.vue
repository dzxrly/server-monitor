<template>
  <q-layout view="hHh lpR fff">

    <q-page-container>
      <router-view />

      <q-page-sticky>
        <q-btn
          v-if="!showSettingDialog"
          class="q-ma-md shadow-4"
          color="primary"
          icon="settings"
          size="md"
          @click="showSettingDialog = true"
          round
        />
      </q-page-sticky>
    </q-page-container>

    <q-footer class="bg-transparent text-secondary row justify-center items-center">
      <span>FOOTER</span>
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

  </q-layout>
</template>
<script setup lang="ts">
import SettingDialog from 'components/index-page/setting-dialog.vue';
import { ref } from 'vue';

const showSettingDialog = ref(false);
</script>
