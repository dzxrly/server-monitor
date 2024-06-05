import { defineStore } from 'pinia';
import { Config } from 'src/module/config';
import { LocalStorage, Notify } from 'quasar';
import { i18n } from 'src/boot/i18n';
import { ref } from 'vue';


export const useConfigStore = defineStore('config', () => {
  const config = ref<Config>(new Config());

  function initConfig() {
    const localConfig = LocalStorage.getItem<Config>('config');
    if (localConfig) {
      config.value = localConfig;
    } else {
      config.value = new Config();
      LocalStorage.set('config', config.value);
    }
  }

  function setConfig(newConfig: Config) {
    config.value = newConfig;
    LocalStorage.set('config', config.value);
    Notify.create({
      message: i18n.global.t('settingsSaved').toString(),
      color: 'primary',
      position: 'top',
      icon: 'check',
      timeout: 1000
    });
  }

  function resetConfig() {
    config.value = new Config();
    LocalStorage.set('config', config.value);
    Notify.create({
      message: i18n.global.t('resetSettingSuccess').toString(),
      color: 'primary',
      position: 'top',
      icon: 'check',
      timeout: 1000
    });
  }

  return {
    config,
    initConfig,
    setConfig,
    resetConfig
  };
});
