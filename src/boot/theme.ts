import { defineBoot } from '#q-app';
import { Dark } from 'quasar';
import { watch } from 'vue';

import { useConfigStore } from '@/features/settings/stores/config-store';

export default defineBoot(({ store }) => {
  const configStore = useConfigStore(store);
  configStore.initConfig();

  watch(
    () => configStore.config.darkMode,
    (darkMode) => {
      Dark.set(darkMode);
      document.documentElement.style.colorScheme = darkMode ? 'dark' : 'light';
    },
    { immediate: true },
  );
});
