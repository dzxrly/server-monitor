import { flushPromises, mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import {
  LocalStorage,
  Notify,
  QDialog,
  QForm,
  QInput,
  QSelect,
  Quasar,
} from 'quasar';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { defineComponent, h, nextTick, ref } from 'vue';

import { i18n } from '@/boot/i18n';
import ServerFormDialog from '@/features/servers/components/ServerFormDialog.vue';
import type { AppConfig, ServerConfig } from '@/features/settings/model/config';
import { useConfigStore } from '@/features/settings/stores/config-store';

const first: ServerConfig = {
  uniqueId: 'first-server',
  customName: 'First server',
  serverUrl: 'http://first.invalid:6543',
  tagColor: '#123456',
  gpuServer: { gpuType: 'NVIDIA' },
};
const second: ServerConfig = {
  ...first,
  uniqueId: 'second-server',
  customName: 'Second server',
  serverUrl: 'http://second.invalid:6543',
  gpuServer: { gpuType: 'NoneGPU' },
};
const unmounts: Array<() => void> = [];

function createDialog() {
  const pinia = createPinia();
  setActivePinia(pinia);
  const store = useConfigStore();
  store.initConfig();
  store.config.serverListConfig = structuredClone([first, second]);
  const visible = ref(false);
  const serverId = ref(first.uniqueId);
  const mode = ref<'add' | 'edit'>('edit');
  const wrapper = mount(
    defineComponent({
      setup: () => () =>
        h(
          QDialog,
          {
            modelValue: visible.value,
            'onUpdate:modelValue': (value: boolean) => (visible.value = value),
            transitionDuration: 0,
            noFocus: true,
            noRefocus: true,
          },
          {
            default: () =>
              h(ServerFormDialog, {
                modelValue: visible.value,
                'onUpdate:modelValue': (value: boolean) =>
                  (visible.value = value),
                mode: mode.value,
                serverId: serverId.value,
              }),
          },
        ),
    }),
    {
      attachTo: document.body,
      global: {
        plugins: [[Quasar, { plugins: { LocalStorage, Notify } }], pinia, i18n],
      },
    },
  );
  vi.spyOn(Notify, 'create').mockImplementation(() => () => {});
  unmounts.push(() => wrapper.unmount());
  return {
    wrapper,
    store,
    visible,
    serverId,
    mode,
    form: () => wrapper.getComponent(ServerFormDialog),
    async open() {
      visible.value = true;
      await nextTick();
      await flushPromises();
    },
  };
}

beforeEach(() => {
  localStorage.clear();
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {});
});

afterEach(() => {
  unmounts.splice(0).forEach((unmount) => unmount());
  vi.restoreAllMocks();
  localStorage.clear();
});

describe('server form inside a lazy dialog', () => {
  it('loads the current server on first open and persists edits under the same ID', async () => {
    const dialog = createDialog();
    expect(dialog.wrapper.findComponent(ServerFormDialog).exists()).toBe(false);
    await dialog.open();
    const fields = dialog.form().findAllComponents(QInput);
    expect(fields.map((field) => field.props('modelValue'))).toEqual([
      first.uniqueId,
      first.serverUrl,
      first.customName,
      first.tagColor,
    ]);
    expect(dialog.form().getComponent(QSelect).props('modelValue')).toBe(
      'NVIDIA',
    );
    await fields[1]!.find('input').setValue('http://changed.invalid:6543///');
    await fields[2]!.find('input').setValue('Renamed server');
    await fields[3]!.find('input').setValue('#abcdef');
    dialog
      .form()
      .getComponent(QSelect)
      .vm.$emit('update:modelValue', 'NoneGPU');
    await dialog.form().find('form').trigger('submit');
    await flushPromises();

    expect(dialog.visible.value).toBe(false);
    expect(dialog.store.config.serverListConfig).toEqual([
      {
        ...first,
        customName: 'Renamed server',
        serverUrl: 'http://changed.invalid:6543',
        tagColor: '#abcdef',
        gpuServer: { gpuType: 'NoneGPU' },
      },
      second,
    ]);
    expect(LocalStorage.getItem<AppConfig>('config')?.serverListConfig).toEqual(
      dialog.store.config.serverListConfig,
    );
    expect(Notify.create).toHaveBeenCalledOnce();
    setActivePinia(createPinia());
    const reloadedStore = useConfigStore();
    reloadedStore.initConfig();
    expect(reloadedStore.config.serverListConfig[0]?.customName).toBe(
      'Renamed server',
    );
  });

  it('discards cancelled changes and loads the selected server when reopened', async () => {
    const dialog = createDialog();
    await dialog.open();
    await dialog
      .form()
      .findAllComponents(QInput)[2]!
      .find('input')
      .setValue('Unsaved name');
    await dialog
      .form()
      .findAll('button')
      .find((button) => button.text() === 'Cancel')!
      .trigger('click');
    await vi.waitFor(() =>
      expect(dialog.wrapper.findComponent(ServerFormDialog).exists()).toBe(
        false,
      ),
    );
    await dialog.open();
    expect(
      dialog.form().findAllComponents(QInput)[2]!.props('modelValue'),
    ).toBe(first.customName);
    dialog.serverId.value = second.uniqueId;
    await nextTick();
    expect(
      dialog.form().findAllComponents(QInput)[2]!.props('modelValue'),
    ).toBe(second.customName);
    expect(dialog.store.config.serverListConfig).toEqual([first, second]);
  });

  it('shows an error and disables saving when the target does not exist', async () => {
    const dialog = createDialog();
    dialog.serverId.value = 'missing-server';
    await dialog.open();
    expect(dialog.form().get('[role="alert"]').text()).toBe('Server not found');
    expect(dialog.form().findAllComponents(QInput)).toHaveLength(0);
    expect(
      dialog.form().get('button[type="submit"]').attributes('disabled'),
    ).toBeDefined();
    await dialog.form().find('form').trigger('submit');
    await flushPromises();
    expect(dialog.visible.value).toBe(true);
    expect(dialog.store.config.serverListConfig).toEqual([first, second]);
    expect(Notify.create).not.toHaveBeenCalled();
  });

  it('keeps the dialog open if the server is deleted during validation', async () => {
    const dialog = createDialog();
    await dialog.open();
    let resolve!: (valid: boolean) => void;
    vi.spyOn(
      dialog.form().getComponent(QForm).vm,
      'validate',
    ).mockImplementation(
      () => new Promise<boolean>((done) => (resolve = done)),
    );
    dialog.form().getComponent(QForm).vm.$emit('submit', new Event('submit'));
    dialog.store.deleteServer(first.uniqueId);
    resolve(true);
    await flushPromises();
    expect(dialog.visible.value).toBe(true);
    expect(dialog.form().get('[role="alert"]').text()).toBe('Server not found');
    expect(dialog.store.config.serverListConfig).toEqual([second]);
    expect(Notify.create).not.toHaveBeenCalled();
  });

  it('does not apply a pending save to a different server', async () => {
    const dialog = createDialog();
    await dialog.open();
    let resolve!: (valid: boolean) => void;
    vi.spyOn(
      dialog.form().getComponent(QForm).vm,
      'validate',
    ).mockImplementation(
      () => new Promise<boolean>((done) => (resolve = done)),
    );
    dialog.form().getComponent(QForm).vm.$emit('submit', new Event('submit'));
    dialog.serverId.value = second.uniqueId;
    await nextTick();
    resolve(true);
    await flushPromises();
    expect(dialog.visible.value).toBe(true);
    expect(dialog.store.config.serverListConfig).toEqual([first, second]);
    expect(Notify.create).not.toHaveBeenCalled();
  });

  it.each([null, '', 'x'.repeat(65)])(
    'rejects an invalid name (%s) without closing',
    async (name) => {
      const dialog = createDialog();
      await dialog.open();
      dialog
        .form()
        .findAllComponents(QInput)[2]!
        .vm.$emit('update:modelValue', name);
      await nextTick();
      await dialog.form().find('form').trigger('submit');
      await flushPromises();
      expect(dialog.visible.value).toBe(true);
      expect(dialog.store.config.serverListConfig).toEqual([first, second]);
      expect(Notify.create).not.toHaveBeenCalled();
    },
  );

  it('still creates a server with a new ID in add mode', async () => {
    const dialog = createDialog();
    dialog.mode.value = 'add';
    await dialog.open();
    const fields = dialog.form().findAllComponents(QInput);
    expect(fields[2]!.props('modelValue')).toBe('');
    await fields[2]!.find('input').setValue('New server');
    await dialog.form().find('form').trigger('submit');
    await flushPromises();
    expect(dialog.visible.value).toBe(false);
    expect(dialog.store.config.serverListConfig).toHaveLength(3);
    expect(dialog.store.config.serverListConfig[2]).toMatchObject({
      customName: 'New server',
    });
    expect(dialog.store.config.serverListConfig[2]?.uniqueId).not.toBe(
      first.uniqueId,
    );
  });

  it('reports failed updates and preserves the explicit target ID', () => {
    const { store } = createDialog();
    expect(store.updateServer('missing-server', first)).toBe(false);
    expect(store.config.serverListConfig).toEqual([first, second]);
    expect(
      store.updateServer(first.uniqueId, { ...first, uniqueId: 'wrong-id' }),
    ).toBe(true);
    expect(store.config.serverListConfig).toEqual([first, second]);
  });
});
