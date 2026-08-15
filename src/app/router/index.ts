import { defineRouter } from '#q-app';
import { Notify } from 'quasar';
import { createRouter, createWebHistory } from 'vue-router';

import { i18n } from '@/boot/i18n';
import { useConfigStore } from '@/features/settings/stores/config-store';
import routes from '@/app/router/routes';

export default defineRouter(({ store }) => {
  const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior: () => ({ left: 0, top: 0 }),
  });

  router.beforeEach((to) => {
    if (to.name !== 'ServerDetail') return true;
    const configStore = useConfigStore(store);
    configStore.initConfig();
    const serverId = String(to.params.uid ?? '');
    if (
      configStore.config.serverListConfig.some(
        (server) => server.uniqueId === serverId,
      )
    ) {
      return true;
    }
    Notify.create({
      message: `${i18n.global.t('serverRouteFailed')}${serverId}`,
      type: 'negative',
    });
    return { name: 'Dashboard' };
  });

  return router;
});
