import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        name: 'IndexPage',
        path: '',
        component: () => import('../pages/IndexPage.vue'),
      },
      {
        name: 'ServerDetail',
        path: '/server/:uid',
        component: () => import('../pages/ServerDetailPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/ErrorNotFound.vue'),
  },
];

export default routes;
