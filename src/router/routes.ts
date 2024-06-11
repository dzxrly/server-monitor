import { RouteRecordRaw } from 'vue-router';
import { useConfigStore } from 'stores/user-config';
import { ServerConfig } from 'src/module/config';
import { Notify } from 'quasar';
import { i18n } from 'boot/i18n';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        name: 'IndexPage',
        path: '',
        component: () => import('pages/IndexPage.vue'),
      },
      {
        name: 'ServerDetail',
        path: '/server/:uid',
        component: () => import('pages/ServerDetailPage.vue'),
        beforeEnter: (to) => {
          const configStore = useConfigStore();
          const isRouteSuccess =
            configStore.config.serverListConfig.findIndex(
              (server: ServerConfig) => {
                return (to.params.uid as string) === server.uniqueId;
              }
            ) !== -1;
          if (!isRouteSuccess) {
            Notify.create({
              message: `${i18n.global.t('serverRouteFailed')}${
                to.params.uid as string
              }`,
              type: 'negative',
            });
          }
          return isRouteSuccess;
        },
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
