import { flushPromises, mount } from '@vue/test-utils';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { defineComponent, h, nextTick, ref } from 'vue';

import { fetchMetrics } from '@/features/monitoring/api/metrics-client';
import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import { useServerMetrics } from '@/features/monitoring/composables/use-server-metrics';

vi.mock('@/features/monitoring/api/metrics-client', () => ({
  fetchMetrics: vi.fn(),
}));

interface PendingRequest {
  url: string;
  limit: number;
  signal: AbortSignal;
  resolve: (value: MetricsSnapshot) => void;
  reject: (reason: Error) => void;
}

const requests: PendingRequest[] = [];
const unmounts: Array<() => void> = [];
const snapshot = (sequence: number) => ({ sequence }) as MetricsSnapshot;

function startPolling() {
  const options = {
    serverUrl: ref('http://first.invalid'),
    refreshSeconds: ref(5),
    processLimit: ref(5),
    paused: ref(false),
  };
  let state!: ReturnType<typeof useServerMetrics>;
  const wrapper = mount(
    defineComponent({
      setup() {
        state = useServerMetrics(options);
        return () => h('div');
      },
    }),
  );
  unmounts.push(() => wrapper.unmount());
  return { options, state, wrapper };
}

beforeEach(() => {
  vi.useFakeTimers();
  requests.length = 0;
  vi.mocked(fetchMetrics).mockImplementation(
    (url, limit, signal) =>
      new Promise((resolve, reject) => {
        requests.push({ url, limit, signal: signal!, resolve, reject });
      }),
  );
});

afterEach(() => {
  unmounts.splice(0).forEach((unmount) => unmount());
  vi.useRealTimers();
  vi.clearAllMocks();
});

describe('server metrics polling', () => {
  it('requests a changed URL immediately and ignores an old success', async () => {
    const { options, state } = startPolling();
    const oldRequest = requests[0]!;
    options.serverUrl.value = 'http://second.invalid';
    await nextTick();

    expect(oldRequest.signal.aborted).toBe(true);
    expect(requests.map((request) => request.url)).toEqual([
      'http://first.invalid',
      'http://second.invalid',
    ]);
    oldRequest.resolve(snapshot(1));
    await flushPromises();
    expect(state.metrics.value).toBeUndefined();
    expect(state.refreshing.value).toBe(true);
    expect(state.loading.value).toBe(true);

    requests[1]!.resolve(snapshot(2));
    await flushPromises();
    expect(state.metrics.value?.sequence).toBe(2);
    expect(state.refreshing.value).toBe(false);
    expect(state.loading.value).toBe(false);
  });

  it('does not let an old failure or finalizer overwrite the new request', async () => {
    const { options, state } = startPolling();
    options.serverUrl.value = 'http://second.invalid';
    await nextTick();
    requests[0]!.reject(new Error('old server failed'));
    await flushPromises();
    expect(state.error.value).toBeUndefined();
    expect(state.refreshing.value).toBe(true);
    await state.refresh();
    expect(requests).toHaveLength(2);

    requests[1]!.resolve(snapshot(2));
    await flushPromises();
    expect(state.online.value).toBe(true);
  });

  it('clears the previous server snapshot and errors when changing the URL', async () => {
    const { options, state } = startPolling();
    requests[0]!.resolve(snapshot(1));
    await flushPromises();
    void state.refresh();
    requests[1]!.reject(new Error('connection lost'));
    await flushPromises();
    expect(state.metrics.value?.sequence).toBe(1);
    expect(state.error.value).toBe('connection lost');

    options.serverUrl.value = 'http://second.invalid';
    await nextTick();
    expect(state.metrics.value).toBeUndefined();
    expect(state.error.value).toBeUndefined();
    expect(state.loading.value).toBe(true);
    expect(requests[2]!.url).toBe('http://second.invalid');
  });

  it('pauses an active request and resumes without waiting for it to settle', async () => {
    const { options, state } = startPolling();
    options.paused.value = true;
    await nextTick();
    expect(requests[0]!.signal.aborted).toBe(true);
    expect(state.refreshing.value).toBe(false);
    await vi.advanceTimersByTimeAsync(10_000);
    expect(requests).toHaveLength(1);

    options.serverUrl.value = 'http://second.invalid';
    await nextTick();
    expect(requests).toHaveLength(1);
    options.paused.value = false;
    await nextTick();
    expect(requests[1]!.url).toBe('http://second.invalid');
    requests[1]!.resolve(snapshot(2));
    await flushPromises();
    requests[0]!.resolve(snapshot(1));
    await flushPromises();
    expect(state.metrics.value?.sequence).toBe(2);
  });

  it('uses changed polling settings and keeps one request in flight', async () => {
    const { options, state } = startPolling();
    options.processLimit.value = 10;
    options.refreshSeconds.value = 2;
    await nextTick();
    expect(requests[0]!.signal.aborted).toBe(true);
    expect(requests[1]!.limit).toBe(10);
    await vi.advanceTimersByTimeAsync(4_000);
    expect(requests).toHaveLength(2);

    requests[1]!.resolve(snapshot(2));
    await flushPromises();
    await vi.advanceTimersByTimeAsync(2_000);
    expect(requests).toHaveLength(3);
    expect(state.refreshing.value).toBe(true);
  });

  it('cancels polling on unmount and ignores a late response', async () => {
    const { state, wrapper } = startPolling();
    wrapper.unmount();
    expect(requests[0]!.signal.aborted).toBe(true);
    requests[0]!.resolve(snapshot(1));
    await flushPromises();
    await vi.advanceTimersByTimeAsync(10_000);
    expect(requests).toHaveLength(1);
    expect(state.metrics.value).toBeUndefined();
    expect(state.refreshing.value).toBe(false);
  });
});
