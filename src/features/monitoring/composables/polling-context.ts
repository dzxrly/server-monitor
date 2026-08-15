import type { InjectionKey, Ref } from 'vue';

export const POLLING_PAUSED_KEY: InjectionKey<Ref<boolean>> =
  Symbol('polling-paused');
