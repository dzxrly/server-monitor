import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
  shallowRef,
  watch,
} from 'vue';
import type { Ref } from 'vue';

import { fetchMetrics } from '@/features/monitoring/api/metrics-client';
import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';

interface PollingOptions {
  serverUrl: Ref<string>;
  refreshSeconds: Ref<number>;
  processLimit: Ref<number>;
  paused: Ref<boolean>;
}

export function useServerMetrics(options: PollingOptions) {
  const metrics = shallowRef<MetricsSnapshot>();
  const error = ref<string>();
  const loading = ref(true);
  const refreshing = ref(false);
  let timer: number | undefined;
  let controller: AbortController | undefined;

  async function refresh(): Promise<void> {
    if (options.paused.value || refreshing.value) return;
    refreshing.value = true;
    controller = new AbortController();
    try {
      metrics.value = await fetchMetrics(
        options.serverUrl.value,
        options.processLimit.value,
        controller.signal,
      );
      error.value = undefined;
    } catch (reason) {
      if (!controller.signal.aborted) {
        error.value = reason instanceof Error ? reason.message : String(reason);
      }
    } finally {
      loading.value = false;
      refreshing.value = false;
    }
  }

  function restart(): void {
    if (timer !== undefined) window.clearInterval(timer);
    controller?.abort();
    if (!options.paused.value) {
      void refresh();
      timer = window.setInterval(
        () => void refresh(),
        Math.max(1, options.refreshSeconds.value) * 1000,
      );
    }
  }

  watch(
    [
      options.serverUrl,
      options.refreshSeconds,
      options.processLimit,
      options.paused,
    ],
    restart,
  );
  onMounted(restart);
  onBeforeUnmount(() => {
    if (timer !== undefined) window.clearInterval(timer);
    controller?.abort();
  });

  return {
    metrics,
    error,
    loading,
    refreshing,
    online: computed(() => Boolean(metrics.value) && !error.value),
    refresh,
  };
}
