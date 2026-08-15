import { fileURLToPath } from 'node:url';

import { defineConfig } from '#q-app';

export default defineConfig(() => ({
  boot: ['i18n', 'theme'],
  css: ['app.scss'],
  extras: ['mdi-v7', 'fontawesome-v7', 'roboto-font', 'material-icons'],
  build: {
    target: {
      browser: ['es2022', 'firefox115', 'chrome120', 'safari16'],
      node: 'node24',
    },
    vueRouterMode: 'history',
    typescript: {
      strict: true,
      vueShim: true,
    },
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      src: fileURLToPath(new URL('./src', import.meta.url)),
      boot: fileURLToPath(new URL('./src/boot', import.meta.url)),
    },
  },
  devServer: {
    open: false,
  },
  framework: {
    config: {
      notify: {
        position: 'top',
        timeout: 2000,
      },
    },
    plugins: ['LocalStorage', 'Notify'],
  },
  sourceFiles: {
    router: 'src/app/router/index',
    store: 'src/app/stores/index',
  },
  animations: [],
}));
