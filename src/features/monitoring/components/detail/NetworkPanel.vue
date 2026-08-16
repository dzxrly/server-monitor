<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';
import MetricCard from '@/features/monitoring/components/shared/MetricCard.vue';
import { formatBytes, formatRate } from '@/shared/format/metrics';

const props = defineProps<{ network: MetricsSnapshot['network'] }>();
const { t } = useI18n();
const activeInterfaces = computed(
  () => props.network.interfaces.filter((item) => item.isUp).length,
);
</script>

<template>
  <MetricCard
    class="detail-card"
    icon="mdi-lan"
    :title="t('network')"
    :subtitle="`${activeInterfaces}/${network.interfaces.length} ${t('interfacesActive')}`"
  >
    <div class="network-summary">
      <div>
        <q-icon name="download" color="positive" size="xs" />
        <span>{{ t('download') }}</span>
        <strong>{{ formatRate(network.totals.bytesReceivedPerSecond) }}</strong>
        <small>{{ formatBytes(network.totals.bytesReceived) }}</small>
      </div>
      <div>
        <q-icon name="upload" color="info" size="xs" />
        <span>{{ t('upload') }}</span>
        <strong>{{ formatRate(network.totals.bytesSentPerSecond) }}</strong>
        <small>{{ formatBytes(network.totals.bytesSent) }}</small>
      </div>
    </div>

    <div class="interface-list q-mt-md">
      <q-expansion-item
        v-for="networkInterface in network.interfaces"
        :key="networkInterface.name"
        dense
        dense-toggle
        switch-toggle-side
        header-class="interface-header rounded-borders"
      >
        <template #header>
          <q-item-section avatar>
            <q-icon
              name="mdi-ethernet"
              :color="networkInterface.isUp ? 'positive' : 'secondary'"
            />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ networkInterface.name }}</q-item-label>
            <q-item-label caption class="text-muted-color">
              {{
                networkInterface.speedMbps
                  ? `${networkInterface.speedMbps} Mbps`
                  : t('unknownSpeed')
              }}
            </q-item-label>
          </q-item-section>
          <q-item-section side class="text-card-color">
            <span class="text-caption"
              >↓ {{ formatRate(networkInterface.bytesReceivedPerSecond) }}</span
            >
            <span class="text-caption"
              >↑ {{ formatRate(networkInterface.bytesSentPerSecond) }}</span
            >
          </q-item-section>
        </template>
        <div class="interface-detail">
          <div
            v-for="address in networkInterface.addresses"
            :key="`${address.family}-${address.address}`"
            class="address-row"
          >
            <span class="text-uppercase text-caption text-muted-color">{{
              address.family
            }}</span>
            <span class="ellipsis">{{ address.address }}</span>
          </div>
          <div class="row justify-between text-caption q-mt-sm">
            <span
              >{{ t('packets') }} ↓ {{ networkInterface.packetsReceived }}</span
            >
            <span>↑ {{ networkInterface.packetsSent }}</span>
          </div>
        </div>
      </q-expansion-item>
      <div
        v-if="network.interfaces.length === 0"
        class="empty-state text-muted-color"
      >
        {{ t('noNetworkData') }}
      </div>
    </div>
  </MetricCard>
</template>

<style scoped lang="scss">
.network-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;

  > div {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 0.15rem 0.45rem;
    padding: 0.65rem;
    border-radius: 12px;
    background: var(--bg-section-color);
  }

  strong,
  small {
    grid-column: 2;
  }

  small {
    color: var(--text-muted-color);
  }
}

.interface-list {
  display: grid;
  gap: 0.35rem;
}

.interface-header {
  background: var(--bg-section-color);
}

.interface-detail {
  margin: 0.2rem 0 0.5rem;
  padding: 0.65rem;
  border-radius: 12px;
  background: var(--bg-section-strong-color);
}

.address-row {
  display: grid;
  grid-template-columns: 3.5rem minmax(0, 1fr);
  gap: 0.5rem;
}

@media (max-width: 480px) {
  .network-summary {
    grid-template-columns: 1fr;
  }
}
</style>
