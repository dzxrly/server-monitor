<template>
  <q-layout view="hHh lpR fff">

    <q-page-container>
      <router-view />

      <q-page-sticky>
        <div class="q-ma-md column justify-center items-center no-wrap">
          <q-btn
            class="shadow-4"
            color="primary"
            :icon="pauseFetch ? 'play_arrow' : 'pause'"
            size="md"
            @click="pauseFetch = !pauseFetch"
            round
          />
          <q-btn
            class="shadow-4 q-mt-md"
            color="primary"
            icon="settings"
            size="md"
            @click="showSettingDialog = true"
            round
          />
        </div>
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
import { provide, ref } from 'vue';

const showSettingDialog = ref(false);
const pauseFetch = ref<boolean>(false);

provide('pauseFetch', pauseFetch);
</script>
