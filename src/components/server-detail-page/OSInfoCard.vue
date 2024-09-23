<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

const props = defineProps({
  osName: {
    type: String,
    default: 'Unknown',
  },
  osArchitecture: {
    type: String,
    default: 'Unknown',
  },
  osSign: {
    type: String,
    default: 'Unknown',
  },
  osNode: {
    type: String,
    default: 'Unknown',
  },
  osBits: {
    type: String,
    default: 'Unknown',
  },
  osKernel: {
    type: String,
    default: 'Unknown',
  },
});

const { t } = useI18n();
const getOSIcon = computed(() => {
  if (props.osSign === 'Windows') {
    return 'fa-brands fa-windows';
  } else if (props.osSign === 'Linux') {
    return 'fa-brands fa-linux';
  } else return 'desktop_windows';
});
</script>

<template>
  <div
    class="os-info-wrapper bg-card-color full-width column justify-center items-center no-wrap rounded-borders q-pa-md"
  >
    <div class="row justify-between items-center full-width no-wrap">
      <div class="row justify-start items-center full-width no-wrap">
        <q-icon class="q-mr-xs" :name="getOSIcon" size="xs" />
        <span class="text-card-color text-subtitle2 overflow-hidden ellipsis">{{
          t('osCardTitle')
        }}</span>
      </div>
    </div>
    <div
      class="row justify-between items-center full-width no-wrap q-mt-md text-card-color text-body2"
    >
      <span>{{ t('osNameTitle') }}</span
      ><span>{{ props.osName }} {{ props.osBits }}</span>
    </div>
    <div
      class="row justify-between items-center full-width no-wrap q-mt-md text-card-color text-body2"
    >
      <span>{{ t('osArchitectureTitle') }}</span
      ><span>{{ props.osArchitecture }}</span>
    </div>
    <div
      class="row justify-between items-center full-width no-wrap q-mt-md text-card-color text-body2"
    >
      <span>{{ t('deviceNameTitle') }}</span
      ><span>{{ props.osNode }}</span>
    </div>
    <div
      class="row justify-between items-center full-width no-wrap q-mt-md text-card-color text-body2"
    >
      <span>{{ t('osKernel') }}</span
      ><span>{{ props.osKernel }}</span>
    </div>
  </div>
</template>

<style scoped lang="sass"></style>
