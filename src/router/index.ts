import { route } from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';

import routes from './routes';
import { useConfigStore } from 'stores/user-config';
import { ServerConfig } from 'src/module/config';
import { Notify } from 'quasar';
import { i18n } from 'src/boot/i18n';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  Router.beforeEach((to) => {
    if (to.name === 'ServerDetail') {
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
        // change to index page
        return {
          name: 'IndexPage',
        };
      } else return isRouteSuccess;
    }
  });

  return Router;
});
