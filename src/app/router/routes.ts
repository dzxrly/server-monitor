import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/app/layouts/MainLayout.vue'),
    children: [
      {
        name: 'Dashboard',
        path: '',
        component: () =>
          import('@/features/monitoring/pages/DashboardPage.vue'),
      },
      {
        name: 'ServerDetail',
        path: 'server/:uid',
        component: () =>
          import('@/features/monitoring/pages/ServerDetailPage.vue'),
      },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue'),
  },
];

export default routes;
