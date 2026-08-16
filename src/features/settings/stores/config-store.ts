import { defineStore } from 'pinia';
import { LocalStorage, Notify } from 'quasar';
import { ref, watch } from 'vue';

import { i18n } from '@/boot/i18n';
import {
  type AppConfig,
  type ServerConfig,
  createDefaultConfig,
  normalizeConfig,
} from '@/features/settings/model/config';

const STORAGE_KEY = 'config';

export const useConfigStore = defineStore('config', () => {
  const config = ref<AppConfig>(createDefaultConfig());
  const initialized = ref(false);

  watch(
    config,
    (value) => {
      if (initialized.value) LocalStorage.set(STORAGE_KEY, value);
    },
    { deep: true },
  );

  function initConfig(): void {
    if (initialized.value) return;
    config.value = normalizeConfig(LocalStorage.getItem(STORAGE_KEY));
    initialized.value = true;
    LocalStorage.set(STORAGE_KEY, config.value);
  }

  function setConfig(value: AppConfig, notify = true): void {
    config.value = normalizeConfig(value);
    if (notify) {
      Notify.create({
        message: String(i18n.global.t('settingsSaved')),
        color: 'primary',
        icon: 'check',
        timeout: 1000,
      });
    }
  }

  function addServer(server: ServerConfig): void {
    config.value.serverListConfig.push(server);
  }

  function updateServer(server: ServerConfig): void {
    const index = config.value.serverListConfig.findIndex(
      (candidate) => candidate.uniqueId === server.uniqueId,
    );
    if (index >= 0) config.value.serverListConfig[index] = server;
  }

  function deleteServer(serverId: string): void {
    config.value.serverListConfig = config.value.serverListConfig.filter(
      (server) => server.uniqueId !== serverId,
    );
  }

  function resetConfig(): void {
    config.value = createDefaultConfig();
    Notify.create({
      message: String(i18n.global.t('resetSettingSuccess')),
      color: 'primary',
      icon: 'check',
      timeout: 1000,
    });
  }

  return {
    config,
    initialized,
    initConfig,
    setConfig,
    addServer,
    updateServer,
    deleteServer,
    resetConfig,
  };
});
