<template>
  <q-layout view="hHh lpR fff">

    <q-page-container>
      <router-view />

      <q-page-sticky>
        <div class="q-ma-md column justify-center items-center no-wrap">
          <q-btn
            class="sticky-btn shadow-4 text-btn-color"
            color="btn-color"
            :icon="pauseFetch ? 'play_arrow' : 'pause'"
            size="md"
            @click="pauseFetch = !pauseFetch"
            round
          />
          <q-btn
            class="sticky-btn shadow-4 q-mt-md text-btn-color"
            color="btn-color"
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
import SettingDialog from 'components/index-page/SettingDialog.vue';
import { provide, ref } from 'vue';
import { openURL } from 'quasar';

const showSettingDialog = ref(false);
const pauseFetch = ref<boolean>(false);

provide('pauseFetch', pauseFetch);
</script>

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

.footer-author, .project-row
  text-decoration: none

.footer-author:hover, .project-row:hover
  text-decoration: underline

@keyframes sticky-btn-hide
  0%
    opacity: 1
  100%
    opacity: 0.2
</style>
