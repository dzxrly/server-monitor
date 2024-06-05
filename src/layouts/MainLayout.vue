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

    <q-footer class="bg-transparent text-secondary column justify-center items-center q-py-xs">
      <div class="row justify-center items-center full-width">
        <div class="row justify-center items-center">
          <q-icon class="q-mr-xs" name="mdi-license" size="xs" />
          <span class="q-mr-md">Apache License 2.0</span>
        </div>
        <div
          class="project-row row justify-center items-center cursor-pointer"
          @click="openURL('https://github.com/dzxrly/server-monitor')"
        >
          <q-icon class="q-mr-xs" name="fa-brands fa-github" size="xs" />
          <span>GITHUB</span>
        </div>
      </div>
      <div class="row justify-center items-center full-width">
        <span>by&nbsp;</span>
        <span
          class="footer-author cursor-pointer"
          @click="openURL('https://dzxrly.github.io/')"
        >Egg Targaryen</span>
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

  </q-layout>
</template>
<script setup lang="ts">
import SettingDialog from 'components/index-page/setting-dialog.vue';
import { provide, ref } from 'vue';
import { openURL } from 'quasar';

const showSettingDialog = ref(false);
const pauseFetch = ref<boolean>(false);

provide('pauseFetch', pauseFetch);
</script>

<style lang="sass" scoped>
.footer-author, .project-row
  text-decoration: none

.footer-author:hover, .project-row:hover
  text-decoration: underline
</style>
