import { defineStore } from 'pinia';
import { UserConfig } from 'src/module/user-config';
import { LocalStorage, Notify } from 'quasar';
import { i18n } from 'src/boot/i18n';


export const useUserConfigStore = defineStore('userConfig', {
  state: () => {
    return {
      userConfig: new UserConfig()
    };
  },
  getters: {
    getUserConfig: (state) => state.userConfig
  },
  actions: {
    setUserConfig(newConfig: UserConfig) {
      this.userConfig = newConfig;
    },
    initUserConfigFromLocalStorage() {
      const localConfig = LocalStorage.getItem<UserConfig>('userConfig');
      if (localConfig) {
        this.userConfig = localConfig;
      } else {
        this.userConfig = new UserConfig();
      }
    },
    updateUserConfigToLocalStorage() {
      LocalStorage.set('userConfig', this.userConfig);
      Notify.create({
        message: i18n.global.t('settingsSaved'),
        color: 'primary',
        position: 'top',
        icon: 'check',
        timeout: 1000
      });
    }
  }
});
