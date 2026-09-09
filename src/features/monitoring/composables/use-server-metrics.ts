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
    const request = new AbortController();
    controller = request;
    try {
      const snapshot = await fetchMetrics(
        options.serverUrl.value,
        options.processLimit.value,
        request.signal,
      );
      if (controller !== request || request.signal.aborted) return;
      metrics.value = snapshot;
      error.value = undefined;
    } catch (reason) {
      if (controller === request && !request.signal.aborted) {
        error.value = reason instanceof Error ? reason.message : String(reason);
      }
    } finally {
      if (controller === request) {
        controller = undefined;
        loading.value = false;
        refreshing.value = false;
      }
    }
  }

  function stop(): void {
    if (timer !== undefined) window.clearInterval(timer);
    timer = undefined;
    controller?.abort();
    controller = undefined;
    refreshing.value = false;
  }

  function restart(): void {
    stop();
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
    ([serverUrl], [previousUrl]) => {
      if (serverUrl !== previousUrl) {
        metrics.value = undefined;
        error.value = undefined;
        loading.value = true;
      }
      restart();
    },
  );
  onMounted(restart);
  onBeforeUnmount(stop);

  return {
    metrics,
    error,
    loading,
    refreshing,
    online: computed(() => Boolean(metrics.value) && !error.value),
    refresh,
  };
}
