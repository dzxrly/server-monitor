import { defineBoot } from '#q-app';
import { createI18n } from 'vue-i18n';

import messages from '@/i18n';

const browserLanguage = navigator.language as keyof typeof messages;
export const i18n = createI18n({
  locale: Object.hasOwn(messages, browserLanguage) ? browserLanguage : 'en-US',
  fallbackLocale: 'en-US',
  legacy: false,
  messages,
});

export default defineBoot(({ app }) => {
  app.use(i18n);
});

export const languageMap: Record<string, string> = {
  'en-US': 'English',
  'zh-CN': '简体中文',
  'zh-TW': '繁體中文',
};
